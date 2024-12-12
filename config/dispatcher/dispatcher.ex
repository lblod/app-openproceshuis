defmodule Dispatcher do
  use Matcher
  define_accept_types [
    html: ["text/html", "application/xhtml+html"],
    json: ["application/json", "application/vnd.api+json"],
    upload: ["multipart/form-data"],
    sparql_json: ["application/sparql-results+json"],
    any: [ "*/*" ],
  ]

  define_layers [ :api, :frontend, :not_found ]

  match "/processes/*path",  %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/processes/"
  end

  match "/bpmn-elements",  %{ accept: [:json], layer: :api } do
    Proxy.forward conn, [], "http://cache/bpmn-elements/"
  end

  match "/bpmn-element-types", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, [], "http://cache/bpmn-element-types/"
  end

  post "/bpmn",  %{ accept: [:any], layer: :api } do
    Proxy.forward conn, [], "http://bpmn/"
  end

  ###############################################################
  # files
  ###############################################################

  get "/files/:id/download", %{ accept: [:any], layer: :api } do
    Proxy.forward conn, [], "http://file/files/" <> id <> "/download"
  end

  post "/files/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://file/files/"
  end

  match "/files/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/files/"
  end

  ###############################################################
  # jobs
  ###############################################################

  match "/jobs/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://resource/jobs/"
  end

  ###############################################################
  # reports
  ###############################################################

  post "/reports", %{ accept: [:json], layer: :api } do
    allowed_groups = Plug.Conn.get_req_header(conn, "mu-auth-allowed-groups")
    if Enum.any?(allowed_groups, fn group -> group =~ ~r/"name":"admin"/ end) do
      Proxy.forward(conn, [], "http://report-generation/reports/")
    else
      Plug.Conn.send_resp(conn, 403, "{\"error\":\"Forbidden\"}")
    end
  end

  match "/reports/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://resource/reports/"
  end

  ###############################################################
  # login
  ###############################################################

  match "/sessions/*path", %{ accept: [:json], layer: :api} do
    Proxy.forward conn, path, "http://login/sessions/"
  end

  match "/accounts", %{ accept: [:json], layer: :api} do
    Proxy.forward conn, [], "http://cache/accounts/"
  end

  match "/accounts/*path", %{ accept: [:json], layer: :api} do
    Proxy.forward conn, path, "http://accountdetail/accounts/"
  end

  match "/groups/*path", %{ accept: [:json], layer: :api} do
    Proxy.forward conn, path, "http://cache/groups/"
  end

  match "/sites/*path", %{ accept: [:json], layer: :api} do
    Proxy.forward conn, path, "http://cache/sites/"
  end

  match "/mock/sessions/*path", %{ accept: [:any], layer: :api} do
    Proxy.forward conn, path, "http://mock-login/sessions/"
  end

  match "/impersonations/*path", %{ accept: [:json], layer: :api} do
    Proxy.forward conn, path, "http://impersonation/impersonations/"
  end

  ###############################################################
  # sparql endpoint
  ###############################################################

  post "/sparql/*path", %{ accept: [:sparql_json], layer: :api } do
    Proxy.forward conn, path, "http://database:8890/sparql/"
  end

  ###############################################################
  # search
  ###############################################################

  match "/search/*path", %{  accept: [:json], layer: :api} do
    Proxy.forward conn, path, "http://search/"
  end

  ###############################################################
  # frontend
  ###############################################################

  match "/assets/*path", %{ accept: [:any], layer: :api } do
    Proxy.forward conn, path, "http://frontend/assets/"
  end

  match "/@appuniversum/*path", %{ accept: [:any], layer: :api } do
    Proxy.forward conn, path, "http://frontend/@appuniversum/"
  end

  match "/*_path", %{ accept: [:html], layer: :api } do
    Proxy.forward conn, [], "http://frontend/index.html"
  end

  ###############################################################
  # errors
  ###############################################################

  match "/*_path", %{ accept: [:any], layer: :not_found} do
    send_resp( conn, 404, "{\"error\": {\"code\": 404}")
  end
end
