FROM node:20

RUN corepack enable && corepack prepare pnpm@latest --activate

# Set the working directory in the container
WORKDIR /usr/src/app
COPY package.json .
COPY pnpm-workspace.yaml .
COPY .app/package.json .app/
COPY .demo/package.json .demo/

# Install dependencies using pnpm
RUN command -v pnpm || npm install -g pnpm
COPY . .
RUN pnpm install
RUN pnpm build
CMD ["node", ".app/.output/server/index.mjs"]
#RUN node .app/.output/server/index.mjs

