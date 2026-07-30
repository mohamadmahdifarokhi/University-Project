FROM node:20

RUN corepack enable && corepack prepare pnpm@latest --activate

# Set the working directory in the container
WORKDIR /usr/src/app
COPY package.json .
COPY pnpm-workspace.yaml .
COPY .app/package.json .app/

# Install dependencies using pnpm
RUN command -v pnpm || npm install -g pnpm
COPY . .
RUN pnpm install

# Development is the default for this university project. The source directory
# is bind-mounted by Docker Compose, so Nuxt/Vite can hot-reload every edit.
CMD ["pnpm", "exec", "nuxi", "dev", ".app", "--host", "0.0.0.0", "--port", "3000"]
