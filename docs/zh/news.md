---
layout: page
title: 新闻动态
lang: zh
sidebar: false
---

<ul class="news-list">
  {% assign current_lang = page.lang | default: 'en' %}
  {% assign lang_posts = site.posts | where: "lang", current_lang %}
  {% for post in lang_posts %}
  <li class="news-item">
    <span class="news-date">{{ post.date | date: "%Y-%m-%d" }}</span>
    <a href="{{ post.url | relative_url }}" class="news-title">{{ post.title }}</a>
  </li>
  {% endfor %}
</ul>