function ensureHtmlDeps()
  quarto.doc.addHtmlDependency({
    name = 'lordicon-bundle',
    version = '1.9.0',
    scripts = {'assets/js/bundle.js'}
  })
end

function buildElement(src, colors, stroke, trigger, target, state, delay, class, style)

  if colors ~= '' then
    colors = 'colors="' .. colors .. '" '
  end

  if stroke ~= '' then
      stroke = 'stroke="' .. stroke .. '" '
  end

  if trigger ~= '' then
    trigger = 'trigger="' .. trigger .. '" '
  end
  
  if target ~= '' then
    target = 'target="' .. target .. '" '  
  end

  if state ~= '' then
    state = 'state="' .. state .. '" '
  end

  if delay ~= '' then
    delay = 'delay="' .. delay .. '" '
  end
  
  if class ~= '' then
    class = 'class="' .. class .. '" '
  end
  
  if style ~= '' then
    style = 'style="' .. style .. '" '
  end
  
  -- detect html
  if quarto.doc.isFormat("html:js") then
    ensureHtmlDeps()
    return pandoc.RawInline('html', '<lord-icon ' .. src .. colors .. stroke .. trigger .. target .. state .. delay .. class .. style .. '></lord-icon>')
  else
    return pandoc.Null()
  end
  
end

function li(args, kwargs)
  local code = pandoc.utils.stringify(args[1])
  local colors = pandoc.utils.stringify(kwargs['colors'])
  local stroke = pandoc.utils.stringify(kwargs['stroke'])
  local trigger = pandoc.utils.stringify(kwargs['trigger'])
  local target = pandoc.utils.stringify(kwargs['target'])
  local state = pandoc.utils.stringify(kwargs['state'])
  local delay = pandoc.utils.stringify(kwargs['delay'])
  local class = pandoc.utils.stringify(kwargs['class'])
  local style = pandoc.utils.stringify(kwargs['style'])
  local src = 'src="https://cdn.lordicon.com/' .. code .. '.json" '
  return buildElement(src, colors, stroke, trigger, target, state, delay, class, style)
end


function lif(args, kwargs)
  local file = pandoc.utils.stringify(args[1])
  local colors = pandoc.utils.stringify(kwargs['colors'])
  local stroke = pandoc.utils.stringify(kwargs['stroke'])
  local trigger = pandoc.utils.stringify(kwargs['trigger'])
  local target = pandoc.utils.stringify(kwargs['target'])
  local state = pandoc.utils.stringify(kwargs['state'])
  local delay = pandoc.utils.stringify(kwargs['delay'])
  local class = pandoc.utils.stringify(kwargs['class'])
  local style = pandoc.utils.stringify(kwargs['style'])
  local src = 'src="' .. file .. '" '
  return buildElement(src, colors, stroke, trigger, target, state, delay, class, style)
end
