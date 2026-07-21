---
layout: page
title: News
lang: en
permalink: /news/
sidebar: false
---

<ul class="news-list">
  {% for post in site.posts %}
  <li class="news-item">
    <span class="news-date">{{ post.date | date: "%Y-%m-%d" }}</span>
    <a href="{{ post.url | relative_url }}" class="news-title">{{ post.title }}</a>
  </li>
  {% endfor %}
</ul>
