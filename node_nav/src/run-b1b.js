import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { dijkstra, nearestFacility } from "./pathfind.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const graphPath = join(__dirname, "..", "data", "f1_b_graph.json");
const graph = JSON.parse(readFileSync(graphPath, "utf8"));

function labels(pathIds) {
  return pathIds.map((id) => {
    const n = graph.nodes.find((x) => x.id === id);
    return n ? `${id}（${n.label}）` : id;
  });
}

// 示例：从 136前门 到 洗手间
const toWash = dijkstra(graph, "room137_front", "washroom");
console.log("微机室前门 → 洗手间");
console.log("  距离:", toWash.distance);
console.log("  路径:", labels(toWash.pathNodeIds).join(" → "));

const stairN = nearestFacility(graph, "mobile_room", "楼梯");
console.log("\n移动计算实验室 → 最近「楼梯」类设施");
console.log(stairN);
