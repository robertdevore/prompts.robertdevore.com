(function() {
	var menuButton = document.querySelector('[data-docs-menu]');
	var primaryNavigation = document.getElementById('primary-navigation');
	var menuOverlay = document.querySelector('[data-menu-overlay]');
	if (menuButton && primaryNavigation && menuOverlay) {
		var setMenuOpen = function(isOpen, restoreFocus) {
			menuOverlay.classList.toggle('is-open', isOpen);
			menuOverlay.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
			document.documentElement.classList.toggle('docs-menu-open', isOpen);
			menuButton.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
			menuButton.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
			if (isOpen) {
				window.requestAnimationFrame(function() {
					var closeButton = menuOverlay.querySelector('.menu-overlay-close');
					if (closeButton) {
						closeButton.focus();
					}
				});
			} else if (restoreFocus) {
				menuButton.focus();
			}
		};

		menuButton.addEventListener('click', function() {
			setMenuOpen(menuButton.getAttribute('aria-expanded') !== 'true', false);
		});

		primaryNavigation.querySelectorAll('a').forEach(function(link) {
			link.addEventListener('click', function() {
				setMenuOpen(false, false);
			});
		});
		menuOverlay.querySelectorAll('[data-docs-menu-close]').forEach(function(button) {
			button.addEventListener('click', function() {
				setMenuOpen(false, true);
			});
		});

		document.addEventListener('keydown', function(event) {
			if (menuButton.getAttribute('aria-expanded') !== 'true') {
				return;
			}
			if (event.key === 'Escape') {
				event.preventDefault();
				setMenuOpen(false, true);
				return;
			}
			if (event.key !== 'Tab') {
				return;
			}
			var focusable = Array.prototype.slice.call(menuOverlay.querySelectorAll('a, button'))
				.filter(function(element) { return !element.disabled && element.offsetParent !== null; });
			if (!focusable.length) {
				return;
			}
			var first = focusable[0];
			var last = focusable[focusable.length - 1];
			if (event.shiftKey && document.activeElement === first) {
				event.preventDefault();
				last.focus();
			} else if (!event.shiftKey && document.activeElement === last) {
				event.preventDefault();
				first.focus();
			}
		});
	}

	document.querySelectorAll('.docs-sidebar a').forEach(function(link) {
		var currentPath = window.location.pathname.replace(/index\.html$/, '');
		var linkPath = new URL(link.href, window.location.origin).pathname.replace(/index\.html$/, '');
		if (currentPath === linkPath || (linkPath !== '/' && currentPath.indexOf(linkPath) === 0)) {
			link.setAttribute('aria-current', 'page');
		}
	});

	var input = document.getElementById('docs-search');
	var panel = document.getElementById('docs-search-results');
	var index = [];
	var indexRequest = fetch('/assets/js/docs-search-index.json')
		.then(function(response) { return response.ok ? response.json() : {items: []}; })
		.then(function(payload) {
			index = payload.items || [];
			return index;
		})
		.catch(function() {
			index = [];
			return index;
		});

	var render = function(items, query) {
		if (!panel) {
			return;
		}
		if (!query) {
			panel.classList.remove('is-open');
			panel.innerHTML = '';
			return;
		}
		if (!items.length) {
			panel.replaceChildren();
			var empty = document.createElement('p');
			empty.className = 'docs-search-empty';
			empty.textContent = 'No prompts found.';
			panel.appendChild(empty);
			panel.classList.add('is-open');
			return;
		}
		var fragment = document.createDocumentFragment();
		items.slice(0, 8).forEach(function(item) {
			var description = item.description || item.section || item.route || '';
			var link = document.createElement('a');
			var title = document.createElement('strong');
			var summary = document.createElement('span');
			link.href = item.url;
			title.textContent = item.title;
			summary.textContent = description;
			link.append(title, summary);
			fragment.appendChild(link);
		});
		panel.replaceChildren(fragment);
		panel.classList.add('is-open');
	};

	var search = function(query) {
		var q = query.trim().toLowerCase();
		if (!q) {
			return [];
		}
		return index.filter(function(item) {
			var haystack = [
				item.title,
				item.description,
				item.section,
				item.audience,
				item.difficulty,
				item.status,
				item.version,
				(item.categories || []).join(' '),
				(item.tags || []).join(' '),
				(item.headings || []).join(' '),
				item.text
			].join(' ').toLowerCase();
			return haystack.indexOf(q) >= 0;
		});
	};

	if (input && panel) {
		input.addEventListener('input', function() {
			render(search(input.value), input.value.trim());
		});
		input.addEventListener('keydown', function(event) {
			if (event.key === 'Escape') {
				input.value = '';
				render([], '');
			}
		});
		document.addEventListener('click', function(event) {
			if (!panel.contains(event.target) && event.target !== input) {
				panel.classList.remove('is-open');
			}
		});
	}

	var categoryPage = document.querySelector('[data-prompt-category]');
	if (categoryPage) {
		var category = (categoryPage.getAttribute('data-prompt-category') || '').trim().toLowerCase();
		var categoryResults = categoryPage.querySelector('[data-category-results]');
		var categoryStatus = categoryPage.querySelector('[data-category-status]');
		var renderCategoryCard = function(item) {
			var card = document.createElement('li');
			card.className = 'listing-card';

			var imageLink = document.createElement('a');
			imageLink.className = 'listing-card-image-link';
			imageLink.href = item.url;
			imageLink.setAttribute('aria-label', 'View ' + item.title);
			if (item.featured_image) {
				var image = document.createElement('img');
				image.className = 'listing-card-image';
				image.src = item.featured_image;
				image.alt = item.title;
				image.loading = 'lazy';
				imageLink.appendChild(image);
			} else {
				var placeholder = document.createElement('span');
				placeholder.className = 'listing-card-image-placeholder';
				placeholder.setAttribute('aria-hidden', 'true');
				imageLink.appendChild(placeholder);
			}

			var body = document.createElement('div');
			body.className = 'listing-card-body';
			var tags = document.createElement('div');
			tags.className = 'listing-card-tags';
			(item.tags || []).slice(0, 3).forEach(function(label) {
				var tag = document.createElement('span');
				tag.className = 'tag';
				tag.textContent = label;
				tags.appendChild(tag);
			});
			var title = document.createElement('h2');
			title.className = 'listing-card-title';
			var titleLink = document.createElement('a');
			titleLink.href = item.url;
			titleLink.textContent = item.title;
			title.appendChild(titleLink);
			var excerpt = document.createElement('p');
			excerpt.className = 'listing-card-excerpt';
			excerpt.textContent = item.description || '';
			var action = document.createElement('a');
			action.className = 'listing-card-button';
			action.href = item.url;
			action.textContent = 'Read Prompt';
			body.append(tags, title, excerpt, action);
			card.append(imageLink, body);
			return card;
		};

		indexRequest.then(function(items) {
			var matches = items.filter(function(item) {
				return (item.categories || []).some(function(value) {
					return String(value).toLowerCase() === category;
				});
			});
			categoryResults.replaceChildren();
			matches.forEach(function(item) {
				categoryResults.appendChild(renderCategoryCard(item));
			});
			categoryResults.setAttribute('aria-busy', 'false');
			if (matches.length) {
				categoryStatus.hidden = true;
			} else {
				categoryStatus.textContent = 'No prompts in this category yet. Check back soon.';
			}
		});
	}

	var legacyCopyText = function(text) {
		return new Promise(function(resolve, reject) {
			var textarea = document.createElement('textarea');
			textarea.value = text;
			textarea.setAttribute('readonly', '');
			textarea.style.position = 'fixed';
			textarea.style.opacity = '0';
			document.body.appendChild(textarea);
			textarea.select();
			try {
				if (!document.execCommand('copy')) {
					throw new Error('Copy command was rejected');
				}
				resolve();
			} catch (error) {
				reject(error);
			} finally {
				document.body.removeChild(textarea);
			}
		});
	};

	var copyText = function(text) {
		return legacyCopyText(text).catch(function() {
			if (navigator.clipboard && window.isSecureContext) {
				return navigator.clipboard.writeText(text);
			}
			return Promise.reject(new Error('Clipboard access is unavailable'));
		});
	};

	var copyBlockText = function(block) {
		var code = block.matches('code') ? block : block.querySelector('code');
		if (code) {
			return code.textContent;
		}
		var copy = block.cloneNode(true);
		copy.querySelectorAll('button').forEach(function(item) {
			item.remove();
		});
		return copy.textContent;
	};

	var bindCopyButton = function(button, block) {
		button.addEventListener('click', function() {
			copyText(copyBlockText(block)).then(function() {
				button.textContent = 'Copied';
				window.setTimeout(function() { button.textContent = 'Copy'; }, 3000);
			}).catch(function() {
				var selection = window.getSelection();
				var range = document.createRange();
				range.selectNodeContents(block);
				selection.removeAllRanges();
				selection.addRange(range);
				button.textContent = 'Select and copy';
			});
		});
	};

	var escapeCodeToken = function(value) {
		return value
			.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;')
			.replace(/"/g, '&quot;');
	};

	var highlightJson = function(code) {
		if (code.dataset.jsonHighlighted === 'true') {
			return;
		}
		var source = code.textContent;
		var tokenPattern = /"(?:\\.|[^"\\])*"|\b(?:true|false|null)\b|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?/g;
		var highlighted = '';
		var lastIndex = 0;
		source.replace(tokenPattern, function(token, offset) {
			highlighted += escapeCodeToken(source.slice(lastIndex, offset));
			var tokenClass = 'json-number';
			if (token.charAt(0) === '"') {
				tokenClass = /^\s*:/.test(source.slice(offset + token.length)) ? 'json-key' : 'json-string';
			} else if (token === 'true' || token === 'false') {
				tokenClass = 'json-boolean';
			} else if (token === 'null') {
				tokenClass = 'json-null';
			}
			highlighted += '<span class="json-token ' + tokenClass + '">' + escapeCodeToken(token) + '</span>';
			lastIndex = offset + token.length;
			return token;
		});
		highlighted += escapeCodeToken(source.slice(lastIndex));
		code.innerHTML = highlighted;
		code.dataset.jsonHighlighted = 'true';
	};

	document.querySelectorAll('code.language-json').forEach(highlightJson);

	document.querySelectorAll('[data-copy-code]').forEach(function(button) {
		var container = button.closest('.sk-code-block') || button.parentElement;
		var block = container ? container.querySelector('pre code, pre') : null;
		if (block) {
			bindCopyButton(button, block);
		}
	});

	document.querySelectorAll('.article-body pre').forEach(function(block) {
		if (block.closest('.sk-code-block') && block.closest('.sk-code-block').querySelector('[data-copy-code]')) {
			return;
		}
		if (block.parentElement && block.parentElement.classList.contains('code-block-shell')) {
			return;
		}
		var shell = document.createElement('div');
		var toolbar = document.createElement('div');
		shell.className = 'code-block-shell';
		toolbar.className = 'code-block-toolbar';
		block.parentNode.insertBefore(shell, block);
		shell.appendChild(toolbar);
		shell.appendChild(block);
		var button = document.createElement('button');
		button.type = 'button';
		button.className = 'copy-code-button';
		button.textContent = 'Copy';
		bindCopyButton(button, block);
		toolbar.appendChild(button);
	});

	document.querySelectorAll('.docs-body h2, .docs-body h3').forEach(function(heading) {
		if (heading.id) {
			return;
		}
		var slug = heading.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'section';
		var candidate = slug;
		var count = 2;
		while (document.getElementById(candidate)) {
			candidate = slug + '-' + count;
			count += 1;
		}
		heading.id = candidate;
	});
})();
