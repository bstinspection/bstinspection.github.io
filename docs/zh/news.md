---
layout: page
heading: "新闻动态"
title: "公司动态与检验行业资讯"
description: "BST 的服务覆盖扩展、办事机构变动与检验行业观察。按国家与品类整理，供从亚洲采购的进口商参考。"
lang: zh
sidebar: false
---

<ul class="news-list news-table">
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