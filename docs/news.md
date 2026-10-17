---
layout: page
heading: "News"
title: "Inspection News & Market Updates"
description: "Company news, new service coverage and inspection market updates from BST. Country launches and practical notes for importers sourcing in Asia."
lang: en
permalink: /news/
sidebar: false
---

<ul class="news-list">
  {% assign current_lang = page.lang | default: 'en' %}
  {% assign lang_posts = site.posts | where: "lang", current_lang %}
  {% for post in lang_posts %}
  <li class="news-item">
    <span class="news-date">{{ post.date | date: "%Y-%m-%d" }}</span>
    <a href="{{ post.url | relative_url }}" class="news-title">{{ post.heading | default: post.title }}</a>
    <p class="news-excerpt">{{ post.excerpt | strip_html | normalize_whitespace | truncate: 140 }}</p>
  </li>
  {% endfor %}
</ul>
