---
layout: home
title: Home
lang: en
permalink: /
sidebar: false
hero_image: /images/background.jpg?v={{ site.cache_buster }}
---

<section class="section animate-on-scroll">
  <div class="section-title">
    <h2>Our Services</h2>
    <p>BST provides comprehensive quality assurance services throughout your supply chain.</p>
  </div>

  <div class="services-grid">
    <a href="{{ '/services/' | relative_url }}#fa" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-building"></i></div>
      <h3>Factory Audit (FA)</h3>
      <p>Audit manufacturers against quality standards.</p>
    </a>
    <a href="{{ '/services/' | relative_url }}#sca" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-handshake"></i></div>
      <h3>Social Compliance (SCA)</h3>
      <p>Social accountability and code of conduct audits.</p>
    </a>
    <a href="{{ '/services/' | relative_url }}#ipc" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-microchip"></i></div>
      <h3>Initial Production Check (IPC)</h3>
      <p>Check components and materials before mass production.</p>
    </a>
    <a href="{{ '/services/' | relative_url }}#ipqc" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-cogs"></i></div>
      <h3>In-Process Quality Check (IPQC)</h3>
      <p>Early warning of quality issues during production.</p>
    </a>
    <a href="{{ '/services/' | relative_url }}#dupro" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-clipboard-check"></i></div>
      <h3>During Production (DUPRO)</h3>
      <p>Visual check at 20-30% production completion.</p>
    </a>
    <a href="{{ '/services/' | relative_url }}#fri" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-check-double"></i></div>
      <h3>Final Random Inspection (FRI)</h3>
      <p>Pre-shipment inspection on finished goods.</p>
    </a>
    <a href="{{ '/services/' | relative_url }}#ls" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-ship"></i></div>
      <h3>Loading Supervision (L/S)</h3>
      <p>Supervise container loading and sealing.</p>
    </a>
    <a href="{{ '/services/' | relative_url }}#ta" class="service-card">
      <div class="service-icon-wrap"><i class="fas fa-flask"></i></div>
      <h3>Testing Arrangement (TA)</h3>
      <p>Independent lab testing and CE certification.</p>
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
      {% for post in site.posts limit:3 %}
      <li class="news-item">
        <span class="news-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}" class="news-title">{{ post.title }}</a>
      </li>
      {% endfor %}
    </ul>
    <p class="text-center mt-2"><a href="{{ '/news/' | relative_url }}" class="btn btn-primary"><i class="fas fa-newspaper"></i> {{ site.data.i18n[page.lang].news.read_more }}</a></p>
  </div>
</section>

<section class="cta-section animate-on-scroll">
  <div class="container cta-content">
    <h2>{{ site.data.i18n[page.lang].cta.title }}</h2>
    <p>{{ site.data.i18n[page.lang].cta.desc }}</p>
    <a href="{{ '/contact/' | relative_url }}" class="btn"><i class="fas fa-paper-plane"></i> {{ site.data.i18n[page.lang].cta.button }}</a>
  </div>
</section>
