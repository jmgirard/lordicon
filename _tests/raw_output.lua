--[[
  Call the lordicon shortcodes directly, outside a Quarto render, and print
  the raw HTML each one returns. Quarto's HTML post-processing keeps only the
  first of two same-name attributes, so a rendered page cannot show whether
  the filter itself wrote an attribute twice; this output can.

  Usage: quarto pandoc lua _tests/raw_output.lua CASES.json
  CASES.json holds a list of {"shortcode", "arg", "kwargs"} objects. Prints
  one line of HTML per case, in order.
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
  local result = shortcodes[case.shortcode]({ pandoc.Str(case.arg) }, kwargs)
  print(result.text)
end
