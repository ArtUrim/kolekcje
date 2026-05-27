FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY app.vue ./
COPY nuxt.config.ts ./
COPY tsconfig.json ./
COPY assets ./assets
COPY components ./components
COPY composables ./composables
COPY i18n ./i18n
COPY layouts ./layouts
COPY pages ./pages
COPY plugins ./plugins
COPY public ./public
COPY server ./server
COPY types ./types

RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NITRO_HOST=0.0.0.0
ENV NITRO_PORT=3000

EXPOSE 3000

COPY --from=builder /app/.output ./.output

CMD ["node", ".output/server/index.mjs"]
