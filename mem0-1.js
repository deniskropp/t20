import { Memory } from "mem0ai/oss";

const config = {
  enableGraph: true,
  graphStore: {
    provider: "neo4j",
    config: {
      url: process.env.NEO4J_URL,
      username: process.env.NEO4J_USERNAME,
      password: process.env.NEO4J_PASSWORD,
      database: "neo4j",
    },
  },
};

const memory = new Memory(config);

const conversation = [
  { role: "user", content: "Alice met Bob at GraphConf 2025 in San Francisco." },
  { role: "assistant", content: "Great! Logging that connection." },
];

await memory.add(conversation, { userId: "demo-user" });

const results = await memory.search(
  "Who did Alice meet at GraphConf?",
  { userId: "demo-user", limit: 3, rerank: true }
);

results.results.forEach((hit) => {
  console.log(hit.memory);
});