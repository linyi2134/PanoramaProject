import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { dijkstra, nearestFacility } from "./pathfind.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const graphPath = join(__dirname, "..", "data", "building-graph.json");
const graph = JSON.parse(readFileSync(graphPath, "utf8"));

// 示例：从「一楼大厅」到「一楼走廊东口」
const route = dijkstra(graph, "n1", "n2");
console.log("n1 → n2:", route);

// 示例：当前在 n3，找最近的洗手间
const near = nearestFacility(graph, "n3", "洗手间");
console.log("n3 最近洗手间:", near);
