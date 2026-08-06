--[[
  lordicon.lua — Quarto shortcodes for embedding Lordicon animated icons.

  Provides two shortcodes:
    {{< li CODE ... >}}   render an icon from the Lordicon CDN by its code
    {{< lif FILE ... >}}  render an icon from a local Lottie .json file

  Any additional key=value pairs are forwarded verbatim as attributes on the
  <lord-icon> element, so the shortcode automatically tracks the element API
  (colors, stroke, trigger, target, state, delay, speed, loading, class, id,
  style, …). See https://lordicon.com/docs/web for the full attribute list.
]]

-- Cache-busting identifier for the bundled player. Keep in sync with the
-- @lordicon/element version pinned in package.json.
local BUNDLE_VERSION = "2.3.1"

-- Shortcode keys that are handled specially rather than forwarded as-is.
local RESERVED = {
  label = true,
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

-- Build the <lord-icon> element for the given source URL and shortcode kwargs.
local function build_element(src, kwargs)
  -- Icons only render in HTML output that ships JavaScript; skip elsewhere.
  if not quarto.doc.isFormat("html:js") then
    return pandoc.Null()
  end
  ensure_deps()

  local attrs = { string.format('src="%s"', attr_escape(src)) }

  -- Forward every non-reserved kwarg as an attribute, sorted for stable output.
  local keys = {}
  for key in pairs(kwargs) do
    if not RESERVED[key] then
      keys[#keys + 1] = key
    end
  end
  table.sort(keys)

  for _, key in ipairs(keys) do
    local val = value_of(kwargs[key])
    if val ~= "" then
      attrs[#attrs + 1] = string.format('%s="%s"', key, attr_escape(val))
    end
  end

  -- Accessibility: announce the icon when a label is given, otherwise mark it
  -- decorative so assistive technology skips it.
  local label = value_of(kwargs["label"])
  if label ~= "" then
    attrs[#attrs + 1] = string.format('role="img" aria-label="%s"', attr_escape(label))
  else
    attrs[#attrs + 1] = 'aria-hidden="true"'
  end

  return pandoc.RawInline("html", "<lord-icon " .. table.concat(attrs, " ") .. "></lord-icon>")
end

-- {{< li CODE ... >}} — icon from the Lordicon CDN.
local function li(args, kwargs)
  local code = pandoc.utils.stringify(args[1])
  return build_element("https://cdn.lordicon.com/" .. code .. ".json", kwargs)
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
-- that was exported in Lordicon's "Minified" format.
local warned_minified = {}

local function check_minified(file, kwargs)
  if warned_minified[file] then
    return
  end

  local used = {}
  for key in pairs(CONTROL_DEPENDENT) do
    if value_of(kwargs[key]) ~= "" then
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
      "lordicon: %s looks like a Minified Lottie export, so %s will have no "
        .. "effect. Either re-export it as Raw (lordicon.com > Edit and "
        .. "download > format menu > the options icon next to Lottie), or set "
        .. "these in the editor before exporting and drop the argument.",
      file,
      table.concat(used, ", ")
    )
  )
end

-- {{< lif FILE ... >}} — icon from a local Lottie .json file.
local function lif(args, kwargs)
  local file = pandoc.utils.stringify(args[1])
  if quarto.doc.isFormat("html:js") then
    check_minified(file, kwargs)
  end
  return build_element(file, kwargs)
end

return {
  ["li"] = li,
  ["lif"] = lif,
}
