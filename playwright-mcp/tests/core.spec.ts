/**
 * Copyright (c) Microsoft Corporation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { test, expect } from './fixtures.js';

test('browser_navigate', async ({ client, server }) => {
  expect(await client.callTool({
    name: 'browser_navigate',
    arguments: { url: server.HELLO_WORLD },
  })).toHaveTextContent(`
### Ran Playwright code
\`\`\`js
// Navigate to ${server.HELLO_WORLD}
await page.goto('${server.HELLO_WORLD}');
\`\`\`

### Page state
- Page URL: ${server.HELLO_WORLD}
- Page Title: Title
- Page Snapshot:
\`\`\`yaml
- generic [active] [ref=e1]: Hello, world!
\`\`\`
`
  );
});

test('browser_select_option', async ({ client, server }) => {
  server.setContent('/', `
    <title>Title</title>
    <select>
      <option value="foo">Foo</option>
      <option value="bar">Bar</option>
    </select>
  `, 'text/html');

  await client.callTool({
    name: 'browser_navigate',
    arguments: { url: server.PREFIX },
  });

  expect(await client.callTool({
    name: 'browser_select_option',
    arguments: {
      element: 'Select',
      ref: 'e2',
      values: ['bar'],
    },
  })).toHaveTextContent(`
### Ran Playwright code
\`\`\`js
// Select options [bar] in Select
await page.getByRole('combobox').selectOption(['bar']);
\`\`\`

### Page state
- Page URL: ${server.PREFIX}
- Page Title: Title
- Page Snapshot:
\`\`\`yaml
- combobox [ref=e2]:
  - option "Foo"
  - option "Bar" [selected]
\`\`\`
`);
});

test('browser_select_option (multiple)', async ({ client, server }) => {
  server.setContent('/', `
    <title>Title</title>
    <select multiple>
      <option value="foo">Foo</option>
      <option value="bar">Bar</option>
      <option value="baz">Baz</option>
    </select>
  `, 'text/html');

  await client.callTool({
    name: 'browser_navigate',
    arguments: { url: server.PREFIX },
  });

  expect(await client.callTool({
    name: 'browser_select_option',
    arguments: {
      element: 'Select',
      ref: 'e2',
      values: ['bar', 'baz'],
    },
  })).toHaveTextContent(`
### Ran Playwright code
\`\`\`js
// Select options [bar, baz] in Select
await page.getByRole('listbox').selectOption(['bar', 'baz']);
\`\`\`

### Page state
- Page URL: ${server.PREFIX}
- Page Title: Title
- Page Snapshot:
\`\`\`yaml
- listbox [ref=e2]:
  - option "Foo" [ref=e3]
  - option "Bar" [selected] [ref=e4]
  - option "Baz" [selected] [ref=e5]
\`\`\`
`);
});

test('browser_type', async ({ client, server }) => {
  server.setContent('/', `
    <!DOCTYPE html>
    <html>
      <input type='keypress' onkeypress="console.log('Key pressed:', event.key, ', Text:', event.target.value)"></input>
    </html>
  `, 'text/html');

  await client.callTool({
    name: 'browser_navigate',
    arguments: {
      url: server.PREFIX,
    },
  });
  await client.callTool({
    name: 'browser_type',
    arguments: {
      element: 'textbox',
      ref: 'e2',
      text: 'Hi!',
      submit: true,
    },
  });
  expect(await client.callTool({
    name: 'browser_console_messages',
  })).toHaveTextContent(/\[LOG\] Key pressed: Enter , Text: Hi!/);
});

test('browser_type (slowly)', async ({ client, server }) => {
  server.setContent('/', `
    <input type='text' onkeydown="console.log('Key pressed:', event.key, 'Text:', event.target.value)"></input>
  `, 'text/html');

  await client.callTool({
    name: 'browser_navigate',
    arguments: {
      url: server.PREFIX,
    },
  });
  await client.callTool({
    name: 'browser_type',
    arguments: {
      element: 'textbox',
      ref: 'e2',
      text: 'Hi!',
      submit: true,
      slowly: true,
    },
  });
  const response = await client.callTool({
    name: 'browser_console_messages',
  });
  expect(response).toHaveTextContent(/\[LOG\] Key pressed: H Text: /);
  expect(response).toHaveTextContent(/\[LOG\] Key pressed: i Text: H/);
  expect(response).toHaveTextContent(/\[LOG\] Key pressed: ! Text: Hi/);
  expect(response).toHaveTextContent(/\[LOG\] Key pressed: Enter Text: Hi!/);
});

test('browser_resize', async ({ client, server }) => {
  server.setContent('/', `
    <title>Resize Test</title>
    <body>
      <div id="size">Waiting for resize...</div>
      <script>new ResizeObserver(() => { document.getElementById("size").textContent = \`Window size: \${window.innerWidth}x\${window.innerHeight}\`; }).observe(document.body);
      </script>
    </body>
  `, 'text/html');
  await client.callTool({
    name: 'browser_navigate',
    arguments: { url: server.PREFIX },
  });

  const response = await client.callTool({
    name: 'browser_resize',
    arguments: {
      width: 390,
      height: 780,
    },
  });
  expect(response).toContainTextContent(`### Ran Playwright code
\`\`\`js
// Resize browser window to 390x780
await page.setViewportSize({ width: 390, height: 780 });
\`\`\``);
  await expect.poll(() => client.callTool({ name: 'browser_snapshot' })).toContainTextContent('Window size: 390x780');
});

test('old locator error message', async ({ client, server }) => {
  server.setContent('/', `
    <button>Button 1</button>
    <button>Button 2</button>
    <script>
      document.querySelector('button').addEventListener('click', () => {
        document.querySelectorAll('button')[1].remove();
      });
    </script>
  `, 'text/html');

  expect(await client.callTool({
    name: 'browser_navigate',
    arguments: {
      url: server.PREFIX,
    },
  })).toContainTextContent(`
  - button "Button 1" [ref=e2]
  - button "Button 2" [ref=e3]
  `.trim());

  await client.callTool({
    name: 'browser_click',
    arguments: {
      element: 'Button 1',
      ref: 'e2',
    },
  });

  expect(await client.callTool({
    name: 'browser_click',
    arguments: {
      element: 'Button 2',
      ref: 'e3',
    },
  })).toContainTextContent('Ref not found');
});

test('visibility: hidden > visible should be shown', { annotation: { type: 'issue', description: 'https://github.com/microsoft/playwright-mcp/issues/535' } }, async ({ client, server }) => {
  server.setContent('/', `
    <div style="visibility: hidden;">
      <div style="visibility: visible;">
        <button>Button</button>
      </div>
    </div>
  `, 'text/html');

  await client.callTool({
    name: 'browser_navigate',
    arguments: { url: server.PREFIX },
  });

  expect(await client.callTool({
    name: 'browser_snapshot'
  })).toContainTextContent('- button "Button"');
});
