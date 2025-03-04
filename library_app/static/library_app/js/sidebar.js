document.addEventListener('DOMContentLoaded', function() {
  const tabLinks = document.querySelectorAll('.tab-link');
  const tabContents = document.querySelectorAll('.tab-content');
  const searchInput = document.getElementById('user-search');
  const searchResults = document.getElementById('search-results');

  // Event delegation для кнопок дій, всередині карток
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('.action-btn');
    if (btn) {
      e.preventDefault();
      if (btn.classList.contains('add-friend')) {
        const userId = btn.getAttribute('data-user-id');
        fetch(`/ajax/send_friend_request/?user_id=${userId}`)
          .then(response => response.json())
          .then(data => {
            alert(data.message || "Запит на дружбу відправлено");
            // Оновлення інтерфейсу за потребою
          });
      } else if (btn.classList.contains('block-user')) {
        const userId = btn.getAttribute('data-user-id') || btn.getAttribute('data-friendship-id');
        fetch(`/ajax/block_user/?user_id=${userId}`)
          .then(response => response.json())
          .then(data => {
            alert(data.message || "Користувача заблоковано");
          });
      } else if (btn.classList.contains('unblock-user')) {
        const userId = btn.getAttribute('data-user-id');
        fetch(`/ajax/unblock_user/?user_id=${userId}`)
          .then(response => response.json())
          .then(data => {
            alert(data.message || "Користувача розблоковано");
          });
      } else if (btn.classList.contains('accept-request')) {
        const friendshipId = btn.getAttribute('data-friendship-id');
        fetch(`/ajax/respond_friend_request/?friendship_id=${friendshipId}&response=accept`)
          .then(response => response.json())
          .then(data => {
            alert(data.message || "Запит прийнято");
          });
      } else if (btn.classList.contains('decline-request')) {
        const friendshipId = btn.getAttribute('data-friendship-id');
        fetch(`/ajax/respond_friend_request/?friendship_id=${friendshipId}&response=decline`)
          .then(response => response.json())
          .then(data => {
            alert(data.message || "Запит відхилено");
          });
      }
    }
  });

  // Перемикання вкладок
  tabLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      tabLinks.forEach(l => l.classList.remove('active'));
      tabContents.forEach(content => content.classList.remove('active'));

      this.classList.add('active');
      const tabId = this.getAttribute('data-tab');
      const targetTab = document.getElementById(tabId);
      if (targetTab) {
        targetTab.classList.add('active');
        loadTabContent(tabId);
      }
    });
  });

  // Функція, що створює картку користувача з вбудованими кнопками дій
  function createUserCard(user, tabId) {
    const cardContainer = document.createElement('div');
    cardContainer.classList.add('user-card-container');

    // HTML картки: посилання на профіль і блок інформації
    let html = `
      <a href="/profile/${user.id}/" class="user-card-link">
        <div class="user-card">
          <img src="${user.avatar}" alt="Avatar" class="user-avatar">
          <div class="user-info">
            <p class="user-username">${user.username}</p>
            ${user.first_name ? `<p class="user-fullname">${user.first_name} ${user.last_name}</p>` : ''}
          </div>
        </div>
      </a>
      <div class="user-actions">
    `;
    // Додаємо кнопки в залежності від вкладки
    if (tabId === 'search-tab') {
      html += `
        <button class="action-btn add-friend" data-user-id="${user.id}">
          <img src="/static/library_app/images/socialbar/invitation_icon.png" alt="Add Friend">
        </button>
        <button class="action-btn block-user" data-user-id="${user.id}">
          <img src="/static/library_app/images/socialbar/blocked_icon.png" alt="Block">
        </button>
      `;
    } else if (tabId === 'requests-tab') {
      // Очікуємо, що об'єкт містить friendship_id для запиту
      html += `
        <button class="action-btn accept-request" data-friendship-id="${user.friendship_id}">
          <img src="/static/library_app/icons/accept.svg" alt="Accept">
        </button>
        <button class="action-btn decline-request" data-friendship-id="${user.friendship_id}">
          <img src="/static/library_app/icons/decline.svg" alt="Decline">
        </button>
        <button class="action-btn block-user" data-friendship-id="${user.friendship_id}">
          <img src="/static/library_app/icons/block.svg" alt="Block">
        </button>
      `;
    } else if (tabId === 'friends-tab') {
      html += `
        <button class="action-btn block-user" data-user-id="${user.id}">
          <img src="/static/library_app/icons/block.svg" alt="Block">
        </button>
      `;
    } else if (tabId === 'blocked-tab') {
      html += `
        <button class="action-btn unblock-user" data-user-id="${user.id}">
          <img src="/static/library_app/icons/unblock.svg" alt="Unblock">
        </button>
      `;
    }
    html += `</div>`;
    cardContainer.innerHTML = html;
    return cardContainer;
  }

  // Завантаження вмісту вкладки через AJAX
  function loadTabContent(tabId) {
    let url = '';
    if (tabId === 'friends-tab') {
      url = '/ajax/friends/';
    } else if (tabId === 'blocked-tab') {
      url = '/ajax/blocked/';
    } else if (tabId === 'requests-tab') {
      url = '/ajax/friend_requests/';
    }
    if (url) {
      fetch(url)
        .then(response => response.json())
        .then(data => {
          const container = document.getElementById(tabId);
          // Очищуємо контейнер перед додаванням нових карток
          container.innerHTML = '';
          if (data.results && data.results.length > 0) {
            data.results.forEach(item => {
              let card = createUserCard(item, tabId);
              container.appendChild(card);
            });
          } else {
            container.innerHTML = '<p>Немає даних</p>';
          }
        })
        .catch(error => console.error('Error loading tab content:', error));
    }
  }

  // Пошук користувачів
  if (searchInput) {
    let searchTimeout;
    searchInput.addEventListener('keyup', function() {
      clearTimeout(searchTimeout);
      const query = this.value;
      searchTimeout = setTimeout(function() {
        if (query.length > 2) {
          fetch(`/ajax/search_users/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
              searchResults.innerHTML = '';
              if (data.results && data.results.length > 0) {
                data.results.forEach(item => {
                  let card = createUserCard(item, 'search-tab');
                  searchResults.appendChild(card);
                });
              } else {
                searchResults.innerHTML = '<p>Нічого не знайдено</p>';
              }
            })
            .catch(error => console.error('Search error:', error));
        } else {
          searchResults.innerHTML = '';
        }
      }, 300);
    });
  }
});