{% import conf.config as cfg %} 
{% import datetime %} 

<!DOCTYPE html>
<html>
<head>
  <!-- Standard Meta -->
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">

  <!-- Site Properties -->
  <title>Homepage - Semantic</title>
  <link rel="shortcut icon" type="image/x-icon" href="{{ static_url("images/pow_favicon-16x16.png")}}">
  <link rel="stylesheet" type="text/css" href="{{ static_url("css/spectre/spectre.css")}}">
  
  
  <!-- +++++++++++++++++++++++++++++++++++++++++++++++++++ -->
  <!-- the stylesheets from the view will be included here -->
  <!-- +++++++++++++++++++++++++++++++++++++++++++++++++++ -->
  {% block include_css %}

  {% end %}

  <style type="text/css">

  

  </style>
  <!-- +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
  <!-- the directly embedded css from the view will be included here -->
  <!-- +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->

  {% block view_css %}

  {% end %}
 
</head>

<body>

<!-- Page Contents -->

<!-- +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
<!-- the View content will be rendered here -->
<!-- +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
{% block content %}

{% end %}

{% include footer.spc %}

<script src="{{ static_url("js/jquery.min.js")}}"></script>
<script async defer src="https://buttons.github.io/buttons.js"></script>

<!-- +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
<!-- included view javascript files go here -->
<!-- +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
{% block include_js %}

{% end %}

<!-- +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
<!-- the embedded View javascript content will be added here -->
<!-- +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
{% block view_js %}
  
{% end %}

<script>
    $(document).ready(function(){  
      if (typeof view_docready === "function") { 
        // ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        // this calls the views docready function if there is one defined.
        // ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        view_docready();
      }
      
    });
</script>





  
</div>  

</body>

</html>
