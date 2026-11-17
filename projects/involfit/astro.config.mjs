import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://involfit.nl',
  trailingSlash: 'always',
  build: { inlineStylesheets: 'never' },
  vite: { build: { assetsInlineLimit: 0 } },
  devToolbar: { enabled: false },
});
