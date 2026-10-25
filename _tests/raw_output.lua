--[[
  Call the lordicon shortcodes directly, outside a Quarto render, and print
  the raw HTML each one returns. Quarto's HTML post-processing keeps only one
  of two same-name attributes, so a rendered page cannot show whether
  the filter itself wrote an attribute twice; this output can.

  Usage: quarto pandoc lua _tests/raw_output.lua CASES.json
  CASES.json holds a list of {"shortcode", "arg", "kwargs"} objects, where a
  null arg calls the shortcode with no first argument. Prints one line of
  HTML per case, in order, and an empty line for a case that returns no HTML.
]]

-- The parts of the quarto API the filter calls, stubbed for HTML output.
quarto = {
  doc = {
    isFormat = function() return true end,
    addHtmlDependency = function() end,
  },
  log = { warning = function() end },
}

local shortcodes = dofile("_extensions/lordicon/lordicon.lua")

local fh = assert(io.open(arg[1], "r"))
local cases = pandoc.json.decode(fh:read("a"), false)
fh:close()

for _, case in ipairs(cases) do
  local kwargs = {}
  for key, value in pairs(case.kwargs) do
    kwargs[key] = pandoc.Inlines({ pandoc.Str(value) })
  end
  local args = {}
  if type(case.arg) == "string" then
    args[1] = pandoc.Str(case.arg)
  end
  local result = shortcodes[case.shortcode](args, kwargs)
  print(result.text or "")
end
