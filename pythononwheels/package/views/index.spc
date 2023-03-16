{% extends "base.spc" %}

{% block content %}
    <!-- Begin page content -->
    <div class="container">
      <!-- The justified navigation menu is meant for single line per list item.
           Multiple lines will require custom code not provided by Bootstrap. -->
      

      <div class="columns" style="padding-top: 20px;">
        <div class="column col-3">
          &nbsp;
        </div>
        <div class="column col-5">
          <a href="/">home</a>
        </div>
        <div class="column col-4">
            <a href="https://www.pythononwheels.org/article/8a729647-47cd-4547-a56e-ee884e3daaef">getting started</a>
        </div>
      </div>
      <div class="columns" style="padding-top: 20px;">
        <div class="column col-5">
            &nbsp;
        </div>
        <div class="column col-2">
              <img src={{ static_url("images/pow_logo_300.png") }}  style="display: inline-block;" />
        </div>
        <div class="column col-5">
        
          &nbsp;
        </div>  
      </div>

      <div class="columns">
        <div class="column col-2">
          &nbsp;
        </div>
        <div class="colum col-8">
          <div class="text-center" style="padding-top: 20px;">
            <h3>Hey! Welcome aboard PythonOnWheels!</h3>
              <h4> The easiest start is to watch the 10 Minute intro video</h4>
              <p></p>
              <iframe width="560" height="315" src="https://www.youtube.com/embed/70Y9GIW0V5M" frameborder="0" 
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
            <p class="lead" style="padding-top: 20px;">
              If you need more info and want to dive deeper just check the <a href="https://www.pythononwheels.org/documentation">documentation</a>
            </p>
            <div>
              Follow on twitter for updates: <a href="https://twitter.com/pythononwheels" class="twitter-follow-button" data-show-count="false">Follow @pythononwheels</a>
              <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');</script>
              Or give it a star if you like. <a class="github-button" href="https://github.com/pythononwheels/pow_devel" data-icon="octicon-star" data-show-count="true" aria-label="Star pythononwheels/pow_devel on GitHub">Star</a>
              <p>
                If you encounter any problems feel very welcome to tweet @pythononwheels or open an <!-- Place this tag where you want the button to render. -->
                <a class="github-button" href="https://github.com/pythononwheels/pow_devel/issues" data-icon="octicon-issue-opened" data-show-count="true" aria-label="Issue pythononwheels/pow_devel on GitHub">issue on github</a>
              </p>
            </div>
          </div>
      <div class="column col-2">
        &nbsp;
      </div>


      

    </div> <!-- /container -->
{% end %}