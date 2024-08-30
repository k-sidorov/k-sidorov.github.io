---
layout: page
permalink: /education/
title: education
description: 
nav: true
nav_order: 6
---

## Project supervision

<div class="students">
    <p>I have been involved in several thesis projects as a daily supervisor.</p>
    {%- assign theses = site.data.supervision | group_by: "type" -%}
    {% for type in theses %}
        <div class="theses">
            <h4><b>{{ type.name }}</b></h4>
            {%- assign thesesTypes = type.items | sort: "year" | reverse -%}
            {% for thesis in thesesTypes %}
                <div class="thesis">
                    {% if type.name == "MSc theses" %}
                        {% if thesis.post_name %}
                            <h5><a href="{{ thesis.link }}" class="{{ thesis.status }}" target="_blank">{{ thesis.topic }}</a></h5>
                            <p> {{ thesis.name }} ({{ thesis.year }})</p>
                        {% else %}
                            <h5><a href="{{ thesis.link }}" class="{{ thesis.status }}" target="_blank">{{ thesis.topic }} ({{ thesis.year }})</a></h5>
                        {% endif %}
                        {{ thesis.abstract }} 
                    {% else %}
                        <h5>{{ thesis.topic }} ({{ thesis.year }})</h5>
                        {{ thesis.abstract }}
                    {% endif %}
                    <div class="keywords">
                        {% for key in thesis.keywords %}
                            <div class="abstract btn btn-sm z-depth-0 keyword">
                                {{ key }}
                            </div>
                        {% endfor %}
                    </div>
                    {% if type.name == "BSc theses" %}
                        <ul>
                            {% for project in thesis.subprojects %}
                                <li><a href="{{ project.link }}" target="_blank">{{ project.title }}</a></li>
                            {% endfor %}
                        </ul>
                    {% endif %}
                </div>  
            {% endfor %}
            <br>
        </div>
    {% endfor %}
</div>

