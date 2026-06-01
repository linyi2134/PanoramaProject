/**
 * 浏览器版 Dijkstra（与 node_nav/src/pathfind.js 逻辑一致）
 */
(function (global) {
  function dijkstra(graph, startId, endId) {
    const nodeIds = new Set(graph.nodes.map((n) => n.id));
    if (!nodeIds.has(startId) || !nodeIds.has(endId)) {
      throw new Error("起点或终点不在 nodes 中");
    }

    const adj = new Map();
    for (const id of nodeIds) adj.set(id, []);
    for (const e of graph.edges) {
      const w = Number(e.weight);
      adj.get(e.from).push({ to: e.to, w });
      adj.get(e.to).push({ to: e.from, w });
    }

    const dist = new Map();
    const prev = new Map();
    for (const id of nodeIds) {
      dist.set(id, Infinity);
      prev.set(id, null);
    }
    dist.set(startId, 0;

    const pq = [{ id: startId, d: 0 }];
    const seen = new Set();

    while (pq.length) {
      pq.sort((a, b) => a.d - b.d);
      const { id: u, d } = pq.shift();
      if (seen.has(u)) continue;
      seen.add(u);
      if (u === endId) break;

      for (const { to: v, w } of adj.get(u)) {
        const nd = d + w;
        if (nd < dist.get(v)) {
          dist.set(v, nd);
          prev.set(v, u);
          pq.push({ id: v, d: nd });
        }
      }
    }

    if (dist.get(endId) === Infinity) {
      return { distance: Infinity, pathNodeIds: [] };
    }

    const pathNodeIds = [];
    for (let at = endId; at != null; at = prev.get(at)) {
      pathNodeIds.push(at);
    }
    pathNodeIds.reverse();
    return { distance: dist.get(endId), pathNodeIds };
  }

  global.IndoorPathfind = { dijkstra };
})(typeof window !== "undefined" ? window : globalThis);
