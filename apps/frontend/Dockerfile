FROM node:20-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app

# Copy workspace package files
COPY package*.json ./
COPY packages/core/package*.json ./packages/core/
COPY apps/frontend/package*.json ./apps/frontend/

# Install dependencies
RUN npm install

# Build @sixfinger/core
FROM deps AS builder
WORKDIR /app
COPY packages/core ./packages/core
WORKDIR /app/packages/core
RUN npm run build

# Build frontend
WORKDIR /app
COPY apps/frontend ./apps/frontend
WORKDIR /app/apps/frontend
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nodejs /app/apps/frontend/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/frontend/.next/static ./apps/frontend/.next/static
COPY --from=builder --chown=nextjs:nodejs /app/apps/frontend/public ./apps/frontend/public

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "apps/frontend/server.js"]
