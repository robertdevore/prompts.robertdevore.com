document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('pre > code').forEach((codeBlock, index) => {
    const pre = codeBlock.parentElement;

    // Wrap pre/code in a container div
    const wrapper = document.createElement('div');
    wrapper.className = 'code-wrapper';
    wrapper.style.position = 'relative';

    // Insert the wrapper and move pre into it
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    // Create the copy button
    const button = document.createElement('button');
    button.className = 'copy-btn';
    button.innerText = 'Copy';
    button.setAttribute('data-code-id', index);

    // Click event
    button.addEventListener('click', () => {
      const text = codeBlock.innerText;
      navigator.clipboard.writeText(text).then(() => {
        button.innerText = 'Copied!';
        setTimeout(() => {
          button.innerText = 'Copy';
        }, 2000);
      }).catch(() => {
        button.innerText = 'Failed';
      });
    });

    // Position and insert button
    button.style.position = 'absolute';
    button.style.top = '8px';
    button.style.right = '8px';
    wrapper.appendChild(button);
  });
});
