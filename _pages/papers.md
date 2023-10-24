---
layout: archive
title: "Papers"
permalink: /papers/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

## Manuscripts
{% for post in site.manuscripts reversed %}
  {% include archive-single.html %}
{% endfor %}

## Publications
{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}

## Dissertation
{% for post in site.dissertation reversed %}
  {% include archive-single.html %}
{% endfor %}
