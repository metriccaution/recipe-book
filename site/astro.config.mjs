import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static',
  site: process.env.SITE_URL ?? 'https://metriccaution.github.io',
  base: process.env.BASE_PATH ?? '/recipe-book',
});
