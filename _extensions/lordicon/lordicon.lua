function ensureHtmlDeps()
  quarto.doc.addHtmlDependency({
    name = 'lord-icon-element',
    version = '3.4.0',
    scripts = {'assets/js/bundle.js'},
    stylesheets = {'assets/css/styles.css'}
  })
end


return {
  ["li"] = function(args, kwargs)
    local code = pandoc.utils.stringify(args[1])
    -- detect html
    if quarto.doc.isFormat("html:js") then
      ensureHtmlDeps()
      return pandoc.RawInline('html', '<lord-icon src="https://cdn.lordicon.com/' .. code .. '.json" trigger="loop" style="width:250px;height:250px;"></lord-icon>')
    else
      return pandoc.Null()
    end

  end
}
