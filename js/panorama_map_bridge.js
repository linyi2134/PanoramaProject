/**
 * 二维地图节点 ↔ 全景场景对照
 *
 * B区（二栋）1–4：1西南 2西北 3东南 4东北
 * A区（一栋）2–5F 1–5：1南侧楼梯 2东南 3西南 4西北 5东北
 * A区 1F 仅 1–2：1西北分叉 2南侧楼梯
 * 连廊 1–5F：统一 → outdoor_stair 户外楼梯
 */
(function (global) {
  const NODE_LABELS = {
    fork_sw: "西南分叉",
    fork_nw: "西北分叉",
    fork_se: "东南分叉",
    fork_ne: "东北分叉",
    stair_south: "南侧楼梯",
    outdoor_stair: "户外楼梯",
  };

  const B_PANO_SUFFIX = {
    1: "fork_sw",
    2: "fork_nw",
    3: "fork_se",
    4: "fork_ne",
  };

  /** A 座 2F–5F */
  const A_PANO_SUFFIX = {
    1: "stair_south",
    2: "fork_se",
    3: "fork_sw",
    4: "fork_nw",
    5: "fork_ne",
  };

  /** A 座 1F 仅两个全景场景 */
  const A1_PANO_SUFFIX = {
    1: "fork_nw",
    2: "stair_south",
  };

  const LINK_STAIR = "outdoor_stair";

  function parseNavNodeId(id) {
    let m = id.match(/^b(\d)_(.+)$/);
    if (m) return { zone: "b", floor: +m[1], local: m[2], tab: +m[1] };
    m = id.match(/^a(\d)_(.+)$/);
    if (m) return { zone: "a", floor: +m[1], local: m[2], tab: +m[1] + 7 };
    m = id.match(/^lk(\d)_(.+)$/);
    if (m) return { zone: "lk", floor: +m[1], local: m[2], tab: +m[1] + 13 };
    return null;
  }

  function aSuffixMap(floor) {
    return floor === 1 ? A1_PANO_SUFFIX : A_PANO_SUFFIX;
  }

  function zoneTabLabel(zone, floor) {
    if (zone === "b") return `B${floor}F`;
    if (zone === "a") return `A${floor}F`;
    return `连廊${floor}F`;
  }

  function buildMapNode(zone, floor, local, sceneId) {
    const prefix = zone === "b" ? `b${floor}` : zone === "a" ? `a${floor}` : `lk${floor}`;
    const tab = zone === "b" ? floor : zone === "a" ? floor + 7 : floor + 13;
    return {
      navNodeId: `${prefix}_${local}`,
      tab,
      floor,
      zone,
      local,
      label: NODE_LABELS[local] || local,
      zoneLabel: zoneTabLabel(zone, floor),
      sceneId,
    };
  }

  function nodeToPanoramaScene(navNodeId) {
    const p = parseNavNodeId(navNodeId);
    if (!p) return null;

    if (p.zone === "lk" && p.local === LINK_STAIR) {
      return `连廊-${p.floor}f`;
    }

    if (p.zone === "b") {
      const entry = Object.entries(B_PANO_SUFFIX).find(([, fork]) => fork === p.local);
      if (!entry) return null;
      return `二栋-${p.floor}f-${entry[0]}`;
    }

    if (p.zone === "a") {
      const map = aSuffixMap(p.floor);
      const entry = Object.entries(map).find(([, loc]) => loc === p.local);
      if (!entry) return null;
      return `一栋-${p.floor}f-${entry[0]}`;
    }

    return null;
  }

  function panoramaSceneToMapNode(sceneId) {
    let m = sceneId.match(/^连廊-(\d)f$/);
    if (m) {
      const floor = +m[1];
      return buildMapNode("lk", floor, LINK_STAIR, sceneId);
    }

    m = sceneId.match(/^二栋-(\d)f-(\d)$/);
    if (m) {
      const floor = +m[1];
      const suf = +m[2];
      const local = B_PANO_SUFFIX[suf];
      if (!local) return null;
      return buildMapNode("b", floor, local, sceneId);
    }

    m = sceneId.match(/^一栋-(\d)f-(\d+)$/);
    if (m) {
      const floor = +m[1];
      const suf = +m[2];
      const local = aSuffixMap(floor)[suf];
      if (!local) return null;
      return buildMapNode("a", floor, local, sceneId);
    }

    return null;
  }

  function hasPanoramaLink(navNodeId) {
    return !!nodeToPanoramaScene(navNodeId);
  }

  function mapUrlForStart(navNodeId) {
    return `map.html?start=${encodeURIComponent(navNodeId)}`;
  }

  function panoramaUrlForScene(sceneId) {
    return `panorama_full.html?scene=${encodeURIComponent(sceneId)}`;
  }

  global.PanoramaMapBridge = {
    NODE_LABELS,
    B_PANO_SUFFIX,
    A_PANO_SUFFIX,
    A1_PANO_SUFFIX,
    parseNavNodeId,
    nodeToPanoramaScene,
    bNodeToPanoramaScene: nodeToPanoramaScene,
    panoramaSceneToMapNode,
    hasPanoramaLink,
    mapUrlForStart,
    panoramaUrlForScene,
  };
})(typeof window !== "undefined" ? window : globalThis);
