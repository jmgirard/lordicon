function ensureHtmlDeps()
  quarto.doc.addHtmlDependency({
    name = 'lord-icon-bundle',
    version = '3.4.4',
    scripts = {'assets/js/bundle.js'}
  })
end


function li(args, kwargs)
  local code = pandoc.utils.stringify(args[1])
  local trigger = pandoc.utils.stringify(kwargs['trigger'])
  local speed = pandoc.utils.stringify(kwargs['speed'])
  local delay = pandoc.utils.stringify(kwargs['delay'])
  local colors = pandoc.utils.stringify(kwargs['colors'])
  local stroke = pandoc.utils.stringify(kwargs['stroke'])
  local scale = pandoc.utils.stringify(kwargs['scale'])
  local x = pandoc.utils.stringify(kwargs['x'])
  local y = pandoc.utils.stringify(kwargs['y'])
  local class = pandoc.utils.stringify(kwargs['class'])
  
  local src = 'src="https://cdn.lordicon.com/' .. code .. '.json" '
  
  if trigger ~= '' then
    trigger = 'trigger="' .. trigger .. '" '
  end
  
  if speed ~= '' then
    speed = 'speed="' .. speed .. '" '
  end
  
  if delay ~= '' then
    delay = 'delay="' .. delay .. '" '
  end
  
  if colors ~= '' then
    colors = 'colors="' .. colors .. '" '
  end
  
  if stroke ~= '' then
    stroke = 'stroke="' .. stroke .. '" '
  end
  
  if scale ~= '' then
    scale = 'scale="' .. scale .. '" '
  end
  
  if x ~= '' then
    x = 'axis-x="' .. x .. '" '
  end
  
  if y ~= '' then
    y = 'axis-y="' .. y .. '" '
  end
  
  if class ~= '' then
    class = 'class="' .. class .. '" '
  end
  
  -- detect html
  if quarto.doc.isFormat("html:js") then
    ensureHtmlDeps()
    return pandoc.RawInline('html', '<lord-icon ' .. speed .. delay .. colors .. stroke .. scale .. x .. y .. class .. src .. trigger .. '></lord-icon>')
  else
    return pandoc.Null()
  end
  
end


function lif(args, kwargs)
  local file = pandoc.utils.stringify(args[1])
  local trigger = pandoc.utils.stringify(kwargs['trigger'])
  local speed = pandoc.utils.stringify(kwargs['speed'])
  local delay = pandoc.utils.stringify(kwargs['delay'])
  local colors = pandoc.utils.stringify(kwargs['colors'])
  local stroke = pandoc.utils.stringify(kwargs['stroke'])
  local scale = pandoc.utils.stringify(kwargs['scale'])
  local x = pandoc.utils.stringify(kwargs['x'])
  local y = pandoc.utils.stringify(kwargs['y'])
  local class = pandoc.utils.stringify(kwargs['class'])
  
  local src = 'src="' .. file .. '" '
  
  if trigger ~= '' then
    trigger = 'trigger="' .. trigger .. '" '
  end
  
  if speed ~= '' then
    speed = 'speed="' .. speed .. '" '
  end
  
  if delay ~= '' then
    delay = 'delay="' .. delay .. '" '
  end
  
  if colors ~= '' then
    colors = 'colors="' .. colors .. '" '
  end
  
  if stroke ~= '' then
    stroke = 'stroke="' .. stroke .. '" '
  end
  
  if scale ~= '' then
    scale = 'scale="' .. scale .. '" '
  end
  
  if x ~= '' then
    x = 'axis-x="' .. x .. '" '
  end
  
  if y ~= '' then
    y = 'axis-y="' .. y .. '" '
  end
  
  if class ~= '' then
    class = 'class="' .. class .. '" '
  end
  
  -- detect html
  if quarto.doc.isFormat("html:js") then
    ensureHtmlDeps()
    return pandoc.RawInline('html', '<lord-icon ' .. speed .. delay .. colors .. stroke .. scale .. x .. y .. class .. src .. trigger .. '></lord-icon>')
  else
    return pandoc.Null()
  end
    
end
