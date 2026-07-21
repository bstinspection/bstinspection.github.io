---
layout: home
title: الرئيسية
lang: ar
sidebar: false
hero_image: /images/background.jpg?v={{ site.cache_buster }}
---

{% assign lang_prefix = '' %}
{% if page.lang and page.lang != 'en' %}
  {% assign lang_prefix = '/' | append: page.lang %}
{% endif %}

{% include hero.html %}

<section class="section animate-on-scroll">
  <div class="section-title">
    <h2>{{ site.data.i18n[page.lang].index_services.title }}</h2>
    <p>{{ site.data.i18n[page.lang].index_services.subtitle }}</p>
  </div>

  <div class="services-grid">
    <a href="{{ lang_prefix }}/services/#fa" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-building"></i></div>
      <h3>{{ site.data.i18n[page.lang].services.fa }}</h3>
      <p>{{ site.data.i18n[page.lang].service_cards.fa_desc }}</p>
    </a>
    <a href="{{ lang_prefix }}/services/#sca" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-handshake"></i></div>
      <h3>{{ site.data.i18n[page.lang].services.sca }}</h3>
      <p>{{ site.data.i18n[page.lang].service_cards.sca_desc }}</p>
    </a>
    <a href="{{ lang_prefix }}/services/#ipc" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-microchip"></i></div>
      <h3>{{ site.data.i18n[page.lang].services.ipc }}</h3>
      <p>{{ site.data.i18n[page.lang].service_cards.ipc_desc }}</p>
    </a>
    <a href="{{ lang_prefix }}/services/#ipqc" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-cogs"></i></div>
      <h3>{{ site.data.i18n[page.lang].services.ipqc }}</h3>
      <p>{{ site.data.i18n[page.lang].service_cards.ipqc_desc }}</p>
    </a>
    <a href="{{ lang_prefix }}/services/#dupro" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-clipboard-check"></i></div>
      <h3>{{ site.data.i18n[page.lang].services.dupro }}</h3>
      <p>{{ site.data.i18n[page.lang].service_cards.dupro_desc }}</p>
    </a>
    <a href="{{ lang_prefix }}/services/#fri" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-check-double"></i></div>
      <h3>{{ site.data.i18n[page.lang].services.fri }}</h3>
      <p>{{ site.data.i18n[page.lang].service_cards.fri_desc }}</p>
    </a>
    <a href="{{ lang_prefix }}/services/#ls" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-ship"></i></div>
      <h3>{{ site.data.i18n[page.lang].services.ls }}</h3>
      <p>{{ site.data.i18n[page.lang].service_cards.ls_desc }}</p>
    </a>
    <a href="{{ lang_prefix }}/services/#ta" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-flask"></i></div>
      <h3>{{ site.data.i18n[page.lang].services.ta }}</h3>
      <p>{{ site.data.i18n[page.lang].service_cards.ta_desc }}</p>
    </a>
  </div>
</section>

<section class="section section-alt animate-on-scroll">
  <div class="container">
    <div class="section-title">
      <h2>{{ site.data.i18n[page.lang].why.title }}</h2>
      <p>{{ site.data.i18n[page.lang].why.subtitle }}</p>
    </div>
    <div class="why-grid">
      <div class="why-card">
        <div class="why-icon expertise"><i class="fas fa-users"></i></div>
        <h3>{{ site.data.i18n[page.lang].why.expertise }}</h3>
        <p>{{ site.data.i18n[page.lang].why.expertise_desc }}</p>
      </div>
      <div class="why-card">
        <div class="why-icon speed"><i class="fas fa-bolt"></i></div>
        <h3>{{ site.data.i18n[page.lang].why.speed }}</h3>
        <p>{{ site.data.i18n[page.lang].why.speed_desc }}</p>
      </div>
      <div class="why-card">
        <div class="why-icon cost"><i class="fas fa-dollar-sign"></i></div>
        <h3>{{ site.data.i18n[page.lang].why.cost }}</h3>
        <p>{{ site.data.i18n[page.lang].why.cost_desc }}</p>
      </div>
      <div class="why-card">
        <div class="why-icon global"><i class="fas fa-globe-asia"></i></div>
        <h3>{{ site.data.i18n[page.lang].why.global }}</h3>
        <p>{{ site.data.i18n[page.lang].why.global_desc }}</p>
      </div>
    </div>
  </div>
</section>

<section class="stats-section animate-on-scroll">
  <div class="container">
    <div class="stats-grid">
      <div class="stat-item">
        <div class="stat-icon"><i class="fas fa-calendar-alt"></i></div>
        <div class="stat-number" data-target="15">0+</div>
        <div class="stat-label">{{ site.data.i18n[page.lang].stats.years }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-icon"><i class="fas fa-map-marked-alt"></i></div>
        <div class="stat-number" data-target="3">0+</div>
        <div class="stat-label">{{ site.data.i18n[page.lang].stats.countries }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-icon"><i class="fas fa-clipboard-list"></i></div>
        <div class="stat-number" data-target="5000">0+</div>
        <div class="stat-label">{{ site.data.i18n[page.lang].stats.projects }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-icon"><i class="fas fa-star"></i></div>
        <div class="stat-number" data-target="98">0+</div>
        <div class="stat-label">{{ site.data.i18n[page.lang].stats.satisfaction }}</div>
      </div>
    </div>
  </div>
</section>

<section class="section animate-on-scroll">
  <div class="container">
    <div class="section-title">
      <h2>{{ site.data.i18n[page.lang].news.title }}</h2>
    </div>
    <ul class="news-list">
      {% assign current_lang = page.lang | default: 'en' %}
      {% assign lang_posts = site.posts | where: "lang", current_lang %}
      {% for post in lang_posts limit:3 %}
      <li class="news-item">
        <span class="news-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}" class="news-title">{{ post.title }}</a>
      </li>
      {% endfor %}
    </ul>
    <p class="text-center mt-2"><a href="{{ lang_prefix }}/news/" class="btn btn-primary"><i class="fas fa-newspaper"></i> {{ site.data.i18n[page.lang].news.read_more }}</a></p>
  </div>
</section>

<section class="cta-section animate-on-scroll">
  <div class="container cta-content">
    <h2>{{ site.data.i18n[page.lang].cta.title }}</h2>
    <p>{{ site.data.i18n[page.lang].cta.desc }}</p>
    <a href="{{ lang_prefix }}/contact/" class="btn"><i class="fas fa-paper-plane"></i> {{ site.data.i18n[page.lang].cta.button }}</a>
  </div>
</section>