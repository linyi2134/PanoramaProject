import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { dijkstra, nearestFacility } from "./pathfind.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const graphPath = join(__dirname, "..", "data", "f1_a_graph.json");
const graph = JSON.parse(readFileSync(graphPath, "utf8"));

// 示例：从「一楼大厅」到「一楼走廊东口」
const route = dijkstra(graph, "washroom", "a_door");
console.log("washroom → a_door:", route);

const near = nearestFacility(graph, "office_room", "洗手间");
console.log("office_room 最近洗手间:", near);
