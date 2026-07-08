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
local BUNDLE_VERSION = "1.11.0"

-- Shortcode keys that are handled specially rather than forwarded as-is.
local RESERVED = {
  label = true,
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

-- {{< lif FILE ... >}} — icon from a local Lottie .json file.
local function lif(args, kwargs)
  local file = pandoc.utils.stringify(args[1])
  return build_element(file, kwargs)
end

return {
  ["li"] = li,
  ["lif"] = lif,
}
