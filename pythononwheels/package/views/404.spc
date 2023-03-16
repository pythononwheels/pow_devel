{% extends "base.sui" %}
{% block content %}
    
    <div class="container">
        <div class="coulmns">
            <div class="columns col-1">
                &nbsp;
            </div>
            <div class="column col-7" >
                <img src={{ static_url("images/404_4.png")}} width="75%"/>
                <p class="ui header">    
                    Hm, maybe you want to restart from 
                    <ul>
                        <li>Where you came from: <a href="{{referer}}">{{referer}}</a> </li>
                        <li>or Home:  <a href="/">Home</a></li>
                    </ul>
                </p>
            </div>
        </div>
        <div class="columns">
            <div class="column col-7">
                
                <div class="ui error message" role="alert">
                    <h1 class="alert-heading">Oh no-This URL cannot be Found. </h1> 
                </div>
                
                {% try %}
                    <div class="ui header message"><b>HTTP Status:</b>  {{status}} </div>
                {% except %}
                {% end %}
                {% try %}
                    <div class="ui error message"><b>Message:</b> {{message}} </div>
                {% except %}
                {% end %}
                {% try %}
                    <div class="ui warning message"><b>URI:</b> {{request.path}} </div>
                {% except %}
                {% end %}
                {% try %}
                    <div class="ui message"><b>Request:</b> {{request}} </div>
                {% except %}
                {% end %}
            </div>
            <div class="column col-1>
                &nbsp;
            </div>
        </div>
    </div>


{% end %}