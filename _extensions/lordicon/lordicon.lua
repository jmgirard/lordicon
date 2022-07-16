function ensureHtmlDeps()
  quarto.doc.addHtmlDependency({
    name = 'lord-icon-element',
    version = '3.4.0',
    scripts = {'https://cdn.lordicon.com/xdjxvujz.js'}
  })
end


return {
  ["li"] = function(args, kwargs)
    local src = pandoc.utils.stringify(args[1])
    -- detect html
    if quarto.doc.isFormat("html:js") then
      ensureHtmlDeps()
      return pandoc.RawInline('html', '<lord-icon src="https://cdn.lordicon.com/' .. src .. '.json" trigger="loop" style="width:250px;height:250px"></lord-icon>')
    else
      return pandoc.Null()
    end

  end
}
