function ensureHtmlDeps()
  quarto.doc.addHtmlDependency({
    name = 'lord-icon-element',
    version = '3.4.0',
    scripts = {'assets/js/lord-icon.js'}
    stylesheets = {'assets/css/styles.css'}
  })
  quarto.doc.addHtmlDependency({
    name = 'lottie-web',
    version = '5.9.4',
    scripts = {'assets/js/lottie.js'}
    stylesheets = {'assets/css/styles.css'}
  })
end


return {
  ["li"] = function(args, kwargs)
    -- Triggers: hover, click, loop, loop-on-hover, morph, and boomerang
    -- The delay argument only applies when trigger is loop or loop-on-hover

    -- required
    local src = pandoc.utils.stringify(args[1])
    -- defaults
    local trigger = "loop"
    local primary = "#121331"
    local secondary = "#08a88a"
    local width = "250px"
    local height = "250px"
    local delay = "2000"
    -- customization
    if #args > 1 then
      trigger = pandoc.utils.stringify(args[2])
    end
    if #args > 2 then
      primary = pandoc.utils.stringfy(args[3])
    end
    if #args > 3 then
      secondary = pandoc.utils.stringify(args[4])
    end
    if #args > 4 then
      width = pandoc.utils.stringify(args[5])
      height = width
    end
    if #args > 5 then
      height = pandoc.utils.stringify(args[6])
    end
    if #args > 6 then
      delay = pandoc.utils.stringify(args[7])
    end
    
    -- detect html
    if quarto.doc.isFormat("html:js") then
      ensureHtmlDeps()
      if trigger == "loop" or trigger == "loop-on-hover" then
        return pandoc.RawInline('html', '<lord-icon src="' .. src .. '" trigger="' .. trigger .. '" delay="' .. delay .. '" colors="primary:' .. primary .. ',secondary:' .. secondary .. ' style="width:' .. width .. ';height:' .. height .. '"></lord-icon>')
      else
        return pandoc.RawInline('html', '<lord-icon src="' .. src .. '" trigger="' .. trigger .. '" colors="primary:' .. primary .. ',secondary:' .. secondary .. ' style="width:' .. width .. ';height:' .. height .. '"></lord-icon>')
      end
    else
      return pandoc.Null()
    end

  end
}
