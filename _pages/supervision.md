---
layout: page
permalink: /supervision/
title: Supervision
description: 
nav: true
nav_order: 6
---

I supervise MSc and BSc thesis projects at TU Delft in constraint programming, search methods, and combinatorial optimization, often aiming for publishable research. On this page, I explain how I work best and what you can expect from me as a supervisor; if you are a prospective student deciding whether you want to work with me, I hope you will find this page informative. Want to get a sense of my previous projects? Then [scroll down](#project-portfolio) for a list of projects I supervise or supervised.

Note: I am not a *responsible professor*. I mentor day-to-day, but official decisions, including your grade or your stay in the program, will require a senior faculty member. What follows is a **written description of how I work best as a supervisor**, rather than a formal set of rules. I have found that being transparent about my style helps students know what to expect and decide whether it suits their way of working.

❓ Want to address a more specific concern? Please check with [supervision FAQ](/supervision/faq).

## Goals

By the end of a project with me, I want you to have:

- An **authentic research experience**, rather than merely doing a coursework.
- **Ownership** of your topic and process.
- A **path to an academic publication**, if feasible given your project output.

## My supervision style

📅 **Weekly meetings** with structured agendas; I am hands-off in terms of format, but please let me know the night before what we will discuss this week.  
🗣️ **Verbal-first** feedback: I deliver most of my comments “live” during a meeting, and we work out together the best way to proceed. Of course, for _critical_ deliverables, such as your thesis draft, I will give written feedback.  
🗒 **Constructive, specific, and high-level** feedback: you will receive many critical comments, but I will ground them in concrete, small-scale examples. I also focus my feedback on high-level concerns (e.g., whether your approach is feasible), rather than on minor, technical details.  
♻️ **Iterative cycle**: write → implement → reflect → improve.  
🤗 **Hands-on support** without micromanagement: I will not write code or text for you, but you may rest assured that I will help out with either if you need it.

## What I expect from you

💬 **Consistent communication**, especially when stuck: remember that I can only help you if you indicate that you need help.  
🤔 **Curiosity, independence, and collaboration**: do not expect me to provide step-by-step instructions – I value independence and critical thinking.   
🪞 **Willingness to reflect and adjust**: any progress requires changing your behavior; if you engage openly, I’ll spend as much time as needed to help you improve.  
🧑‍🔬 **Active participation in writing and experimenting**: I will happily help you set up, execute, and describe a convincing experiment, but if you want to learn it, you will have to do it.

## My commitments to you

The points above describe my supervision style in broad strokes. If you are still feeling unsure about how this works day-to-day, check out the [supervision FAQ](/supervision/faq).

- I take your growth seriously and will support you technically and strategically.
- I will not disappear on you, block your ideas arbitrarily, or shift the goalposts.
- I’ll be honest, constructive, and respectful – and I expect the same.
- If we disagree, I will discuss it openly and work towards a fair solution.


## Project portfolio

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
                            {% if thesis.status == "finished" %}
                            <p> {{ thesis.name }}, graduated in {{ thesis.year }} </p>
                            {% else %}
                            <p> {{ thesis.name }}, started in {{ thesis.year }}</p>
                            {% endif %}
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

