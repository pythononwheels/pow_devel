{% extends "base.spc" %}
{% block content %}
    
    <div class="container"> 
        <div class="columns">
            <div class="column col-1">
                &nbsp;
            </div>
            <div class="column col-7" >
                <img src={{ static_url("images/bug.png")}} width="80%"/>
            </div>
        </div>
        <div class="columns">
            <div class="column col-7">
                <div class="toast toast-error">
                    <h1 class="">Oh no! An Error occured. </h1> 
                </div>
                <p class="text-capitalize">    
                    Sorry, this should not have happended!
                </p>
                {% try %}
                    <div class=""><b>HTTP Status:</b> {{status}} </div>
                {% except %}
                {% end %}
                
                {% try %}
                    <div class=""><b>Message:</b> {{message}} </div>
                {% except %}
                {% end %}
                
                {% try %}
                    <div class=""><b>Data:</b> {{data}} </div>
                {% except %}
                {% end %}
                
                {% try %}
                    <div class=""><b>URI:</b> {{request.path}} </div>
                {% except %}
                {% end %}

                {% try %}
                    <div class=""><b>Request:</b>
                            {{request}} 
                    </div>
                {% except %}
                {% end %}
            </div>
            <div class="column col-1">
                &nbsp;
            </div>
        </div>
    </div>
{% end %}