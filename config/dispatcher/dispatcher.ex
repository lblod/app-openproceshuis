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

  match "/process-statistics/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/process-statistics/"
  end

  match "/information-assets/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/information-assets/"
  end

  match "/administrative-unit-classification-codes", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, [], "http://cache/administrative-unit-classification-codes/"
  end

  ###############################################################
  # API
  ###############################################################

  post "/bpmn",  %{ accept: [:any], layer: :api } do
    Proxy.forward conn, [], "http://bpmn/"
  end

  get "/visio/*path",  %{ accept: [:any], layer: :api } do
    Proxy.forward conn, path, "http://visio/"
  end

  post "/anonymization/*path", %{ accept: [:any], layer: :api } do
    Proxy.forward conn, path, "http://anonymization/"
  end

  ###############################################################
  # inventory
  ###############################################################

  get "/conceptual-processes/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/conceptual-processes/"
  end
  
  post "/conceptual-processes/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/conceptual-processes/"
  end

  get "/process-groups/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/process-groups/"
  end

  get "/process-domains/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/process-domains/"
  end

  get "/process-categories/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/process-categories/"
  end

  ###############################################################
  # ipdc
  ###############################################################

  match "/ipdc-instances", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, [], "http://cache/ipdc-instances/"
  end

  match "/ipdc-concepts", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, [], "http://cache/ipdc-concepts/"
  end

  get "/ipdc-products", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, [], "http://cache/ipdc-products/"
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
    Proxy.forward(conn, [], "http://report-generation/reports/")
  end

  match "/reports/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://resource/reports/"
  end

  ###############################################################
  # login
  ###############################################################

  match "/sessions/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://login/sessions/"
  end

  match "/accounts", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, [], "http://cache/accounts/"
  end

  match "/accounts/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://accountdetail/accounts/"
  end

  match "/groups/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/groups/"
  end

  match "/sites/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://cache/sites/"
  end

  match "/mock/sessions/*path", %{ accept: [:any], layer: :api } do
    Proxy.forward conn, path, "http://mock-login/sessions/"
  end

  match "/impersonations/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://impersonation/impersonations/"
  end

  ###############################################################
  # sparql endpoint
  ###############################################################

  post "/sparql/*path", %{ accept: [:sparql_json], layer: :api } do
    Proxy.forward conn, path, "http://database:8890/sparql/"
  end

  ###############################################################
  # ipdc
  ###############################################################

  get "/ipdc/*path", %{ accept: [:json], layer: :api } do
    Proxy.forward conn, path, "http://ipdc-proxy/"
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

  match "/*_path", %{ accept: [:any], layer: :not_found } do
    send_resp( conn, 404, "{\"error\": {\"code\": 404}")
  end
end
