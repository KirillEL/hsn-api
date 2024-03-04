FROM node:18


COPY . /admin
WORKDIR /admin

COPY package.json ./

RUN npm install


EXPOSE 5173


CMD ["npm", "run", "dev"]

