--[[
  lordicon.lua — Quarto shortcodes for embedding Lordicon animated icons.

  Provides two shortcodes:
    {{< li CODE ... >}}   render an icon from the Lordicon CDN by its code
    {{< lif FILE ... >}}  render an icon from a local Lottie .json file

  Any additional key=value pairs are forwarded verbatim as attributes on the
  <lord-icon> element, so the shortcode automatically tracks the element API
  (colors, stroke, trigger, target, state, delay, speed, loading, class, id,
  style, …). See https://lordicon.com/docs/web for the full attribute list.
  The exceptions are `label`, `src` in any letter case (the first argument
  sets the source), and keys that are not valid attribute names; the last two
  are skipped with a render warning. Keys that differ only in letter case, and
  `label` in another letter case, are forwarded with a render warning. An
  icon with an image role but no name, and not hidden, gets a render warning.
]]

-- Cache-busting identifier for the bundled player. Keep in sync with the
-- @lordicon/element version pinned in package.json.
local BUNDLE_VERSION = "2.3.1"

-- Shortcode keys that are handled specially rather than forwarded as-is.
local RESERVED = {
  label = true,
}

-- A key holding whitespace, a control character, or one of these symbols is
-- not a valid HTML attribute name: written out, it can end the tag early,
-- split into stray attributes, or give an attribute with an invalid name.
-- The byte ranges are spelled out because %s and %c follow the current
-- locale, and under a UTF-8 locale they also match bytes inside letters such
-- as "ß".
-- INVALID_NAME covers space and the ASCII controls; C1_CONTROL covers
-- U+0080 to U+009F, which UTF-8 writes as the byte 194 and a second byte.
local INVALID_NAME = "[\0-\32\127\"'>/=]"
local C1_CONTROL = "\194[\128-\159]"

-- ARIA attributes that, when passed by the user in any letter case, replace
-- the aria-hidden default given to an icon without a label.
local ARIA_OVERRIDES = {
  ["aria-hidden"] = true,
  ["aria-label"] = true,
  ["aria-labelledby"] = true,
  role = true,
}

-- Attributes that only work when the icon's Lottie JSON still carries the
-- "control" null layer (holding the primary/secondary/stroke effects) and its
-- full set of animation layers. lordicon.com's export defaults to "Minified",
-- which bakes the chosen colors and stroke into the shapes and keeps only the
-- selected animation. That is a perfectly good trade for a smaller file when
-- the icon is already styled the way you want; it just cannot be combined with
-- these attributes, which would have nothing left to act on.
local CONTROL_DEPENDENT = {
  colors = true,
  state = true,
  stroke = true,
}

local function ensure_deps()
  quarto.doc.addHtmlDependency({
    name = "lordicon-bundle",
    version = BUNDLE_VERSION,
    scripts = { "assets/js/bundle.js" },
  })
end

-- Escape a value for safe inclusion inside a double-quoted HTML attribute.
local function attr_escape(s)
  return (s
    :gsub("&", "&amp;")
    :gsub('"', "&quot;")
    :gsub("<", "&lt;")
    :gsub(">", "&gt;"))
end

-- Stringify a kwargs value, returning "" when the key was not supplied.
local function value_of(v)
  if v == nil then
    return ""
  end
  return pandoc.utils.stringify(v)
end

-- Lowercase the ASCII letters only. string.lower follows the locale, and in
-- some locales it does not map "I" to "i".
local function ascii_lower(s)
  return (s:gsub("[A-Z]", function(c)
    return string.char(c:byte() + 32)
  end))
end

-- A key that HTML does not allow as an attribute name.
local function invalid_name(key)
  return key == "" or key:find(INVALID_NAME) or key:find(C1_CONTROL)
end

-- Warn that a call skipped some of its keys, naming each one in quotes.
local function warn_skipped(call, keys, reason)
  table.sort(keys)
  local quoted = {}
  for i, key in ipairs(keys) do
    quoted[i] = '"' .. key .. '"'
  end
  quarto.log.warning(
    string.format(
      "lordicon: %s skips the %s %s, because %s",
      call,
      #keys == 1 and "key" or "keys",
      table.concat(quoted, ", "),
      reason
    )
  )
end

-- Quote each key and join them as a list: "a" and "b", or "a", "b", and "c".
local function quote_list(keys)
  local quoted = {}
  for i, key in ipairs(keys) do
    quoted[i] = '"' .. key .. '"'
  end
  if #quoted == 2 then
    return quoted[1] .. " and " .. quoted[2]
  end
  quoted[#quoted] = "and " .. quoted[#quoted]
  return table.concat(quoted, ", ")
end

-- Warn about forwarded keys that differ only in letter case, such as `role`
-- and `Role`. Quarto's HTML post-processing keeps only one value of each such
-- group, for letters outside ASCII too. `keys` is sorted. Keys that lowercase to `label`
-- get the label warning instead.
local function warn_case_clashes(call, keys)
  local groups, order = {}, {}
  for _, key in ipairs(keys) do
    local lowered = pandoc.text.lower(key)
    if lowered ~= "label" then
      if not groups[lowered] then
        groups[lowered] = {}
        order[#order + 1] = lowered
      end
      table.insert(groups[lowered], key)
    end
  end

  local clashes = {}
  for _, lowered in ipairs(order) do
    if #groups[lowered] > 1 then
      clashes[#clashes + 1] = quote_list(groups[lowered])
    end
  end
  if #clashes == 0 then
    return
  end

  local advice
  if #clashes == 1 then
    advice = "only one of their values. Keep one of these keys and remove the others."
  else
    advice = "only one value from each group. Keep one key from each group and "
      .. "remove the others."
  end
  quarto.log.warning(
    string.format(
      "lordicon: %s has keys that differ only in letter case: %s. The page "
        .. "keeps %s",
      call,
      table.concat(clashes, "; "),
      advice
    )
  )
end

-- Warn about forwarded keys such as `Label` that lowercase to `label`. Only a
-- lowercase `label` gives the ARIA attributes, so these keys label nothing.
local function warn_label_case(call, keys)
  local found = {}
  for _, key in ipairs(keys) do
    if pandoc.text.lower(key) == "label" then
      found[#found + 1] = key
    end
  end
  if #found == 0 then
    return
  end
  local named
  if #found == 1 then
    named = 'the key "' .. found[1] .. '"'
  else
    named = "the keys " .. quote_list(found)
  end
  quarto.log.warning(
    string.format(
      "lordicon: %s has %s, but only a lowercase label key labels the icon. "
        .. "Use one lowercase label key.",
      call,
      named
    )
  )
end

-- Attributes that give an icon an accessible name, or remove it from what
-- assistive technology reads, so that an image role needs no warning.
local NAMES_OR_HIDES = {
  ["aria-label"] = true,
  ["aria-labelledby"] = true,
  title = true,
  hidden = true,
  inert = true,
}

-- Warn about an icon that the page gives an image role but no name: a screen
-- reader then announces an image and cannot say what it shows. `keys` is
-- sorted, and for keys that differ only in letter case the page keeps the
-- first, so the check reads that one. A `label` always gives a name.
local function warn_nameless_role(call, keys, kwargs, label)
  if label ~= "" then
    return
  end
  local kept = {}
  for _, key in ipairs(keys) do
    local name = ascii_lower(key)
    if kept[name] == nil then
      kept[name] = value_of(kwargs[key])
    end
  end

  local role = kept["role"]
  if role == nil then
    return
  end
  -- The check reads only the first token of the role. A browser uses the
  -- first role it knows, so a value such as "bogus img" is not caught.
  -- ASCII whitespace is spelled out because %s follows the locale.
  local first = role:match("^[\t\n\f\r ]*([^\t\n\f\r ]+)")
  first = first and ascii_lower(first)
  if first ~= "img" and first ~= "image" then
    return
  end
  local hidden = kept["aria-hidden"]
  if hidden and ascii_lower(hidden) == "true" then
    return
  end
  for name in pairs(NAMES_OR_HIDES) do
    if kept[name] then
      return
    end
  end

  quarto.log.warning(
    string.format(
      'lordicon: %s gives the icon role="%s" but no name, so a screen reader '
        .. "announces an image without saying what it shows. Add a label, such "
        .. 'as label="Bell". If the icon is only decoration, pass '
        .. 'aria-hidden="true" instead.',
      call,
      role
    )
  )
end

-- Build the <lord-icon> element for the given source URL and shortcode kwargs.
-- `call` names the shortcode call, such as {{< li CODE >}}, in warnings.
local function build_element(src, kwargs, call)
  -- Icons only render in HTML output that ships JavaScript; skip elsewhere.
  if not quarto.doc.isFormat("html:js") then
    return pandoc.Null()
  end
  ensure_deps()

  local attrs = { string.format('src="%s"', attr_escape(src)) }

  -- Forward every non-reserved kwarg with a value as an attribute, sorted for
  -- stable output. A src key would give a second src, and an invalid name
  -- would give a broken or stray attribute, so both are skipped with a
  -- warning.
  local keys, src_keys, invalid_keys = {}, {}, {}
  for key, v in pairs(kwargs) do
    if not RESERVED[key] and value_of(v) ~= "" then
      if ascii_lower(key) == "src" then
        src_keys[#src_keys + 1] = key
      elseif invalid_name(key) then
        invalid_keys[#invalid_keys + 1] = key
      else
        keys[#keys + 1] = key
      end
    end
  end
  table.sort(keys)

  if #src_keys > 0 then
    warn_skipped(call, src_keys, "the first argument sets the icon. To show "
      .. "another icon, change the first argument instead.")
  end
  if #invalid_keys > 0 then
    warn_skipped(call, invalid_keys, "an attribute name cannot be empty or "
      .. "hold spaces, control characters, quotes, >, /, or =. Rename the key "
      .. "or remove it.")
  end
  warn_case_clashes(call, keys)
  warn_label_case(call, keys)
  warn_nameless_role(call, keys, kwargs, value_of(kwargs["label"]))

  -- Attribute names ignore letter case, so `passed` records each in lowercase.
  local passed = {}
  for _, key in ipairs(keys) do
    attrs[#attrs + 1] = string.format('%s="%s"', key, attr_escape(value_of(kwargs[key])))
    passed[ascii_lower(key)] = true
  end

  -- Accessibility: announce the icon when a label is given, otherwise mark it
  -- decorative so assistive technology skips it. ARIA attributes the user
  -- passed always win over these defaults.
  local label = value_of(kwargs["label"])
  if label ~= "" then
    if not passed["role"] then
      attrs[#attrs + 1] = 'role="img"'
    end
    if not passed["aria-label"] then
      attrs[#attrs + 1] = string.format('aria-label="%s"', attr_escape(label))
    end
  else
    local overridden = false
    for key in pairs(ARIA_OVERRIDES) do
      if passed[key] then
        overridden = true
      end
    end
    if not overridden then
      attrs[#attrs + 1] = 'aria-hidden="true"'
    end
  end

  return pandoc.RawInline("html", "<lord-icon " .. table.concat(attrs, " ") .. "></lord-icon>")
end

-- {{< li CODE ... >}} — icon from the Lordicon CDN.
local function li(args, kwargs)
  local code = pandoc.utils.stringify(args[1])
  return build_element(
    "https://cdn.lordicon.com/" .. code .. ".json",
    kwargs,
    "{{< li " .. code .. " >}}"
  )
end

-- Open a shortcode file path, trying it as given and then relative to the
-- document being rendered. Returns nil when the file cannot be read, in which
-- case checks that depend on its contents are skipped rather than guessed at.
local function open_icon_file(file)
  local fh = io.open(file, "rb")
  if fh then
    return fh
  end
  local input = quarto.doc.input_file
  local dir = input and input:match("^(.*)[/\\][^/\\]+$")
  if dir then
    return io.open(dir .. "/" .. file, "rb")
  end
  return nil
end

-- Warn once per file when control-dependent attributes are used with an icon
-- that was exported in Lordicon's "Minified" format. The warning names the
-- first such call, such as {{< lif FILE >}}.
local warned_minified = {}

local function check_minified(file, kwargs, call)
  if warned_minified[file] then
    return
  end

  -- Attribute names ignore letter case, so `Colors` works like `colors`. Match
  -- the keys in any letter case and name each one as the user wrote it.
  local used = {}
  for key, v in pairs(kwargs) do
    if CONTROL_DEPENDENT[ascii_lower(key)] and value_of(v) ~= "" then
      used[#used + 1] = key
    end
  end
  if #used == 0 then
    return
  end

  local fh = open_icon_file(file)
  if not fh then
    return
  end
  local content = fh:read("a")
  fh:close()
  if not content or content:find('"nm"%s*:%s*"control"') then
    return
  end

  table.sort(used)
  warned_minified[file] = true
  quarto.log.warning(
    string.format(
      "lordicon: %s uses a file that looks like a Minified Lottie export, so "
        .. "%s will have no effect. Either re-export it as Raw (lordicon.com > "
        .. "Edit and download > format menu > the options icon next to Lottie), "
        .. "or set these in the editor before exporting and drop the argument.",
      call,
      table.concat(used, ", ")
    )
  )
end

-- {{< lif FILE ... >}} — icon from a local Lottie .json file.
local function lif(args, kwargs)
  local file = pandoc.utils.stringify(args[1])
  local call = "{{< lif " .. file .. " >}}"
  if quarto.doc.isFormat("html:js") then
    check_minified(file, kwargs, call)
  end
  return build_element(file, kwargs, call)
end

return {
  ["li"] = li,
  ["lif"] = lif,
}
