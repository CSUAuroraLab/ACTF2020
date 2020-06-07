local command = "/usr/bin/gm convert " .. ngx.var.request_filepath .. " -resize " .. ngx.var.width .. "x" .. ngx.var.height .. " +profile \"*\" " .. ngx.var.request_filepath .. "@" .. ngx.var.width .. "w_" .. ngx.var.height .. "h";
os.execute(command);
ngx.exec(ngx.var.request_uri);
