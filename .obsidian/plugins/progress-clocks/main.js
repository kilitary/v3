"use strict";
var __defProp = Object.defineProperty;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __publicField = (obj, key, value) => {
  __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);
  return value;
};
const obsidian = require("obsidian");
const view = require("@codemirror/view");
const language = require("@codemirror/language");
function noop() {
}
const identity = (x) => x;
function assign(tar, src) {
  for (const k in src)
    tar[k] = src[k];
  return tar;
}
function run(fn) {
  return fn();
}
function blank_object() {
  return /* @__PURE__ */ Object.create(null);
}
function run_all(fns) {
  fns.forEach(run);
}
function is_function(thing) {
  return typeof thing === "function";
}
function safe_not_equal(a, b) {
  return a != a ? b == b : a !== b || (a && typeof a === "object" || typeof a === "function");
}
function is_empty(obj) {
  return Object.keys(obj).length === 0;
}
function create_slot(definition, ctx, $$scope, fn) {
  if (definition) {
    const slot_ctx = get_slot_context(definition, ctx, $$scope, fn);
    return definition[0](slot_ctx);
  }
}
function get_slot_context(definition, ctx, $$scope, fn) {
  return definition[1] && fn ? assign($$scope.ctx.slice(), definition[1](fn(ctx))) : $$scope.ctx;
}
function get_slot_changes(definition, $$scope, dirty, fn) {
  if (definition[2] && fn) {
    const lets = definition[2](fn(dirty));
    if ($$scope.dirty === void 0) {
      return lets;
    }
    if (typeof lets === "object") {
      const merged = [];
      const len = Math.max($$scope.dirty.length, lets.length);
      for (let i = 0; i < len; i += 1) {
        merged[i] = $$scope.dirty[i] | lets[i];
      }
      return merged;
    }
    return $$scope.dirty | lets;
  }
  return $$scope.dirty;
}
function update_slot_base(slot, slot_definition, ctx, $$scope, slot_changes, get_slot_context_fn) {
  if (slot_changes) {
    const slot_context = get_slot_context(slot_definition, ctx, $$scope, get_slot_context_fn);
    slot.p(slot_context, slot_changes);
  }
}
function get_all_dirty_from_scope($$scope) {
  if ($$scope.ctx.length > 32) {
    const dirty = [];
    const length = $$scope.ctx.length / 32;
    for (let i = 0; i < length; i++) {
      dirty[i] = -1;
    }
    return dirty;
  }
  return -1;
}
function exclude_internal_props(props) {
  const result = {};
  for (const k in props)
    if (k[0] !== "$")
      result[k] = props[k];
  return result;
}
function compute_rest_props(props, keys) {
  const rest = {};
  keys = new Set(keys);
  for (const k in props)
    if (!keys.has(k) && k[0] !== "$")
      rest[k] = props[k];
  return rest;
}
function action_destroyer(action_result) {
  return action_result && is_function(action_result.destroy) ? action_result.destroy : noop;
}
const is_client = typeof window !== "undefined";
let now = is_client ? () => window.performance.now() : () => Date.now();
let raf = is_client ? (cb) => requestAnimationFrame(cb) : noop;
const tasks = /* @__PURE__ */ new Set();
function run_tasks(now2) {
  tasks.forEach((task) => {
    if (!task.c(now2)) {
      tasks.delete(task);
      task.f();
    }
  });
  if (tasks.size !== 0)
    raf(run_tasks);
}
function loop(callback) {
  let task;
  if (tasks.size === 0)
    raf(run_tasks);
  return {
    promise: new Promise((fulfill) => {
      tasks.add(task = { c: callback, f: fulfill });
    }),
    abort() {
      tasks.delete(task);
    }
  };
}
function append(target, node) {
  target.appendChild(node);
}
function get_root_for_style(node) {
  if (!node)
    return document;
  const root = node.getRootNode ? node.getRootNode() : node.ownerDocument;
  if (root && root.host) {
    return root;
  }
  return node.ownerDocument;
}
function append_empty_stylesheet(node) {
  const style_element = element("style");
  append_stylesheet(get_root_for_style(node), style_element);
  return style_element.sheet;
}
function append_stylesheet(node, style) {
  append(node.head || node, style);
  return style.sheet;
}
function insert(target, node, anchor) {
  target.insertBefore(node, anchor || null);
}
function detach(node) {
  if (node.parentNode) {
    node.parentNode.removeChild(node);
  }
}
function destroy_each(iterations, detaching) {
  for (let i = 0; i < iterations.length; i += 1) {
    if (iterations[i])
      iterations[i].d(detaching);
  }
}
function element(name) {
  return document.createElement(name);
}
function svg_element(name) {
  return document.createElementNS("http://www.w3.org/2000/svg", name);
}
function text(data) {
  return document.createTextNode(data);
}
function space() {
  return text(" ");
}
function empty() {
  return text("");
}
function listen(node, event, handler, options) {
  node.addEventListener(event, handler, options);
  return () => node.removeEventListener(event, handler, options);
}
function prevent_default(fn) {
  return function(event) {
    event.preventDefault();
    return fn.call(this, event);
  };
}
function attr(node, attribute, value) {
  if (value == null)
    node.removeAttribute(attribute);
  else if (node.getAttribute(attribute) !== value)
    node.setAttribute(attribute, value);
}
function set_svg_attributes(node, attributes) {
  for (const key in attributes) {
    attr(node, key, attributes[key]);
  }
}
function children(element2) {
  return Array.from(element2.childNodes);
}
function set_data(text2, data) {
  data = "" + data;
  if (text2.data === data)
    return;
  text2.data = data;
}
function set_input_value(input, value) {
  input.value = value == null ? "" : value;
}
function custom_event(type, detail, { bubbles = false, cancelable = false } = {}) {
  const e = document.createEvent("CustomEvent");
  e.initCustomEvent(type, bubbles, cancelable, detail);
  return e;
}
const managed_styles = /* @__PURE__ */ new Map();
let active = 0;
function hash(str) {
  let hash2 = 5381;
  let i = str.length;
  while (i--)
    hash2 = (hash2 << 5) - hash2 ^ str.charCodeAt(i);
  return hash2 >>> 0;
}
function create_style_information(doc, node) {
  const info = { stylesheet: append_empty_stylesheet(node), rules: {} };
  managed_styles.set(doc, info);
  return info;
}
function create_rule(node, a, b, duration, delay, ease, fn, uid = 0) {
  const step = 16.666 / duration;
  let keyframes = "{\n";
  for (let p = 0; p <= 1; p += step) {
    const t = a + (b - a) * ease(p);
    keyframes += p * 100 + `%{${fn(t, 1 - t)}}
`;
  }
  const rule = keyframes + `100% {${fn(b, 1 - b)}}
}`;
  const name = `__svelte_${hash(rule)}_${uid}`;
  const doc = get_root_for_style(node);
  const { stylesheet, rules } = managed_styles.get(doc) || create_style_information(doc, node);
  if (!rules[name]) {
    rules[name] = true;
    stylesheet.insertRule(`@keyframes ${name} ${rule}`, stylesheet.cssRules.length);
  }
  const animation = node.style.animation || "";
  node.style.animation = `${animation ? `${animation}, ` : ""}${name} ${duration}ms linear ${delay}ms 1 both`;
  active += 1;
  return name;
}
function delete_rule(node, name) {
  const previous = (node.style.animation || "").split(", ");
  const next = previous.filter(
    name ? (anim) => anim.indexOf(name) < 0 : (anim) => anim.indexOf("__svelte") === -1
  );
  const deleted = previous.length - next.length;
  if (deleted) {
    node.style.animation = next.join(", ");
    active -= deleted;
    if (!active)
      clear_rules();
  }
}
function clear_rules() {
  raf(() => {
    if (active)
      return;
    managed_styles.forEach((info) => {
      const { ownerNode } = info.stylesheet;
      if (ownerNode)
        detach(ownerNode);
    });
    managed_styles.clear();
  });
}
let current_component;
function set_current_component(component) {
  current_component = component;
}
function get_current_component() {
  if (!current_component)
    throw new Error("Function called outside component initialization");
  return current_component;
}
function onMount(fn) {
  get_current_component().$$.on_mount.push(fn);
}
function onDestroy(fn) {
  get_current_component().$$.on_destroy.push(fn);
}
function createEventDispatcher() {
  const component = get_current_component();
  return (type, detail, { cancelable = false } = {}) => {
    const callbacks = component.$$.callbacks[type];
    if (callbacks) {
      const event = custom_event(type, detail, { cancelable });
      callbacks.slice().forEach((fn) => {
        fn.call(component, event);
      });
      return !event.defaultPrevented;
    }
    return true;
  };
}
const dirty_components = [];
const binding_callbacks = [];
let render_callbacks = [];
const flush_callbacks = [];
const resolved_promise = /* @__PURE__ */ Promise.resolve();
let update_scheduled = false;
function schedule_update() {
  if (!update_scheduled) {
    update_scheduled = true;
    resolved_promise.then(flush);
  }
}
function tick() {
  schedule_update();
  return resolved_promise;
}
function add_render_callback(fn) {
  render_callbacks.push(fn);
}
function add_flush_callback(fn) {
  flush_callbacks.push(fn);
}
const seen_callbacks = /* @__PURE__ */ new Set();
let flushidx = 0;
function flush() {
  if (flushidx !== 0) {
    return;
  }
  const saved_component = current_component;
  do {
    try {
      while (flushidx < dirty_components.length) {
        const component = dirty_components[flushidx];
        flushidx++;
        set_current_component(component);
        update(component.$$);
      }
    } catch (e) {
      dirty_components.length = 0;
      flushidx = 0;
      throw e;
    }
    set_current_component(null);
    dirty_components.length = 0;
    flushidx = 0;
    while (binding_callbacks.length)
      binding_callbacks.pop()();
    for (let i = 0; i < render_callbacks.length; i += 1) {
      const callback = render_callbacks[i];
      if (!seen_callbacks.has(callback)) {
        seen_callbacks.add(callback);
        callback();
      }
    }
    render_callbacks.length = 0;
  } while (dirty_components.length);
  while (flush_callbacks.length) {
    flush_callbacks.pop()();
  }
  update_scheduled = false;
  seen_callbacks.clear();
  set_current_component(saved_component);
}
function update($$) {
  if ($$.fragment !== null) {
    $$.update();
    run_all($$.before_update);
    const dirty = $$.dirty;
    $$.dirty = [-1];
    $$.fragment && $$.fragment.p($$.ctx, dirty);
    $$.after_update.forEach(add_render_callback);
  }
}
function flush_render_callbacks(fns) {
  const filtered = [];
  const targets = [];
  render_callbacks.forEach((c) => fns.indexOf(c) === -1 ? filtered.push(c) : targets.push(c));
  targets.forEach((c) => c());
  render_callbacks = filtered;
}
let promise;
function wait() {
  if (!promise) {
    promise = Promise.resolve();
    promise.then(() => {
      promise = null;
    });
  }
  return promise;
}
function dispatch(node, direction, kind) {
  node.dispatchEvent(custom_event(`${direction ? "intro" : "outro"}${kind}`));
}
const outroing = /* @__PURE__ */ new Set();
let outros;
function group_outros() {
  outros = {
    r: 0,
    c: [],
    p: outros
  };
}
function check_outros() {
  if (!outros.r) {
    run_all(outros.c);
  }
  outros = outros.p;
}
function transition_in(block, local) {
  if (block && block.i) {
    outroing.delete(block);
    block.i(local);
  }
}
function transition_out(block, local, detach2, callback) {
  if (block && block.o) {
    if (outroing.has(block))
      return;
    outroing.add(block);
    outros.c.push(() => {
      outroing.delete(block);
      if (callback) {
        if (detach2)
          block.d(1);
        callback();
      }
    });
    block.o(local);
  } else if (callback) {
    callback();
  }
}
const null_transition = { duration: 0 };
function create_bidirectional_transition(node, fn, params, intro) {
  const options = { direction: "both" };
  let config = fn(node, params, options);
  let t = intro ? 0 : 1;
  let running_program = null;
  let pending_program = null;
  let animation_name = null;
  function clear_animation() {
    if (animation_name)
      delete_rule(node, animation_name);
  }
  function init2(program, duration) {
    const d = program.b - t;
    duration *= Math.abs(d);
    return {
      a: t,
      b: program.b,
      d,
      duration,
      start: program.start,
      end: program.start + duration,
      group: program.group
    };
  }
  function go(b) {
    const { delay = 0, duration = 300, easing = identity, tick: tick2 = noop, css } = config || null_transition;
    const program = {
      start: now() + delay,
      b
    };
    if (!b) {
      program.group = outros;
      outros.r += 1;
    }
    if (running_program || pending_program) {
      pending_program = program;
    } else {
      if (css) {
        clear_animation();
        animation_name = create_rule(node, t, b, duration, delay, easing, css);
      }
      if (b)
        tick2(0, 1);
      running_program = init2(program, duration);
      add_render_callback(() => dispatch(node, b, "start"));
      loop((now2) => {
        if (pending_program && now2 > pending_program.start) {
          running_program = init2(pending_program, duration);
          pending_program = null;
          dispatch(node, running_program.b, "start");
          if (css) {
            clear_animation();
            animation_name = create_rule(node, t, running_program.b, running_program.duration, 0, easing, config.css);
          }
        }
        if (running_program) {
          if (now2 >= running_program.end) {
            tick2(t = running_program.b, 1 - t);
            dispatch(node, running_program.b, "end");
            if (!pending_program) {
              if (running_program.b) {
                clear_animation();
              } else {
                if (!--running_program.group.r)
                  run_all(running_program.group.c);
              }
            }
            running_program = null;
          } else if (now2 >= running_program.start) {
            const p = now2 - running_program.start;
            t = running_program.a + running_program.d * easing(p / running_program.duration);
            tick2(t, 1 - t);
          }
        }
        return !!(running_program || pending_program);
      });
    }
  }
  return {
    run(b) {
      if (is_function(config)) {
        wait().then(() => {
          config = config(options);
          go(b);
        });
      } else {
        go(b);
      }
    },
    end() {
      clear_animation();
      running_program = pending_program = null;
    }
  };
}
function get_spread_update(levels, updates) {
  const update2 = {};
  const to_null_out = {};
  const accounted_for = { $$scope: 1 };
  let i = levels.length;
  while (i--) {
    const o = levels[i];
    const n = updates[i];
    if (n) {
      for (const key in o) {
        if (!(key in n))
          to_null_out[key] = 1;
      }
      for (const key in n) {
        if (!accounted_for[key]) {
          update2[key] = n[key];
          accounted_for[key] = 1;
        }
      }
      levels[i] = n;
    } else {
      for (const key in o) {
        accounted_for[key] = 1;
      }
    }
  }
  for (const key in to_null_out) {
    if (!(key in update2))
      update2[key] = void 0;
  }
  return update2;
}
function get_spread_object(spread_props) {
  return typeof spread_props === "object" && spread_props !== null ? spread_props : {};
}
function bind(component, name, callback) {
  const index = component.$$.props[name];
  if (index !== void 0) {
    component.$$.bound[index] = callback;
    callback(component.$$.ctx[index]);
  }
}
function create_component(block) {
  block && block.c();
}
function mount_component(component, target, anchor, customElement) {
  const { fragment, after_update } = component.$$;
  fragment && fragment.m(target, anchor);
  if (!customElement) {
    add_render_callback(() => {
      const new_on_destroy = component.$$.on_mount.map(run).filter(is_function);
      if (component.$$.on_destroy) {
        component.$$.on_destroy.push(...new_on_destroy);
      } else {
        run_all(new_on_destroy);
      }
      component.$$.on_mount = [];
    });
  }
  after_update.forEach(add_render_callback);
}
function destroy_component(component, detaching) {
  const $$ = component.$$;
  if ($$.fragment !== null) {
    flush_render_callbacks($$.after_update);
    run_all($$.on_destroy);
    $$.fragment && $$.fragment.d(detaching);
    $$.on_destroy = $$.fragment = null;
    $$.ctx = [];
  }
}
function make_dirty(component, i) {
  if (component.$$.dirty[0] === -1) {
    dirty_components.push(component);
    schedule_update();
    component.$$.dirty.fill(0);
  }
  component.$$.dirty[i / 31 | 0] |= 1 << i % 31;
}
function init(component, options, instance2, create_fragment2, not_equal, props, append_styles, dirty = [-1]) {
  const parent_component = current_component;
  set_current_component(component);
  const $$ = component.$$ = {
    fragment: null,
    ctx: [],
    props,
    update: noop,
    not_equal,
    bound: blank_object(),
    on_mount: [],
    on_destroy: [],
    on_disconnect: [],
    before_update: [],
    after_update: [],
    context: new Map(options.context || (parent_component ? parent_component.$$.context : [])),
    callbacks: blank_object(),
    dirty,
    skip_bound: false,
    root: options.target || parent_component.$$.root
  };
  append_styles && append_styles($$.root);
  let ready = false;
  $$.ctx = instance2 ? instance2(component, options.props || {}, (i, ret, ...rest) => {
    const value = rest.length ? rest[0] : ret;
    if ($$.ctx && not_equal($$.ctx[i], $$.ctx[i] = value)) {
      if (!$$.skip_bound && $$.bound[i])
        $$.bound[i](value);
      if (ready)
        make_dirty(component, i);
    }
    return ret;
  }) : [];
  $$.update();
  ready = true;
  run_all($$.before_update);
  $$.fragment = create_fragment2 ? create_fragment2($$.ctx) : false;
  if (options.target) {
    if (options.hydrate) {
      const nodes = children(options.target);
      $$.fragment && $$.fragment.l(nodes);
      nodes.forEach(detach);
    } else {
      $$.fragment && $$.fragment.c();
    }
    if (options.intro)
      transition_in(component.$$.fragment);
    mount_component(component, options.target, options.anchor, options.customElement);
    flush();
  }
  set_current_component(parent_component);
}
class SvelteComponent {
  $destroy() {
    destroy_component(this, 1);
    this.$destroy = noop;
  }
  $on(type, callback) {
    if (!is_function(callback)) {
      return noop;
    }
    const callbacks = this.$$.callbacks[type] || (this.$$.callbacks[type] = []);
    callbacks.push(callback);
    return () => {
      const index = callbacks.indexOf(callback);
      if (index !== -1)
        callbacks.splice(index, 1);
    };
  }
  $set($$props) {
    if (this.$$set && !is_empty($$props)) {
      this.$$.skip_bound = true;
      this.$$set($$props);
      this.$$.skip_bound = false;
    }
  }
}
class State {
  constructor() {
    __publicField(this, "debug", false);
    __publicField(this, "sections");
  }
}
/**
 * @license lucide-svelte v0.331.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const defaultAttributes = {
  xmlns: "http://www.w3.org/2000/svg",
  width: 24,
  height: 24,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  "stroke-width": 2,
  "stroke-linecap": "round",
  "stroke-linejoin": "round"
};
const defaultAttributes$1 = defaultAttributes;
function get_each_context$4(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[10] = list[i][0];
  child_ctx[11] = list[i][1];
  return child_ctx;
}
function create_dynamic_element(ctx) {
  let svelte_element;
  let svelte_element_levels = [ctx[11]];
  let svelte_element_data = {};
  for (let i = 0; i < svelte_element_levels.length; i += 1) {
    svelte_element_data = assign(svelte_element_data, svelte_element_levels[i]);
  }
  return {
    c() {
      svelte_element = svg_element(ctx[10]);
      set_svg_attributes(svelte_element, svelte_element_data);
    },
    m(target, anchor) {
      insert(target, svelte_element, anchor);
    },
    p(ctx2, dirty) {
      set_svg_attributes(svelte_element, svelte_element_data = get_spread_update(svelte_element_levels, [dirty & 32 && ctx2[11]]));
    },
    d(detaching) {
      if (detaching)
        detach(svelte_element);
    }
  };
}
function create_each_block$4(ctx) {
  let previous_tag = ctx[10];
  let svelte_element_anchor;
  let svelte_element = ctx[10] && create_dynamic_element(ctx);
  return {
    c() {
      if (svelte_element)
        svelte_element.c();
      svelte_element_anchor = empty();
    },
    m(target, anchor) {
      if (svelte_element)
        svelte_element.m(target, anchor);
      insert(target, svelte_element_anchor, anchor);
    },
    p(ctx2, dirty) {
      if (ctx2[10]) {
        if (!previous_tag) {
          svelte_element = create_dynamic_element(ctx2);
          previous_tag = ctx2[10];
          svelte_element.c();
          svelte_element.m(svelte_element_anchor.parentNode, svelte_element_anchor);
        } else if (safe_not_equal(previous_tag, ctx2[10])) {
          svelte_element.d(1);
          svelte_element = create_dynamic_element(ctx2);
          previous_tag = ctx2[10];
          svelte_element.c();
          svelte_element.m(svelte_element_anchor.parentNode, svelte_element_anchor);
        } else {
          svelte_element.p(ctx2, dirty);
        }
      } else if (previous_tag) {
        svelte_element.d(1);
        svelte_element = null;
        previous_tag = ctx2[10];
      }
    },
    d(detaching) {
      if (detaching)
        detach(svelte_element_anchor);
      if (svelte_element)
        svelte_element.d(detaching);
    }
  };
}
function create_fragment$h(ctx) {
  var _a;
  let svg;
  let each_1_anchor;
  let svg_stroke_width_value;
  let svg_class_value;
  let current;
  let each_value = ctx[5];
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block$4(get_each_context$4(ctx, each_value, i));
  }
  const default_slot_template = ctx[9].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[8], null);
  let svg_levels = [
    defaultAttributes$1,
    ctx[6],
    { width: ctx[2] },
    { height: ctx[2] },
    { stroke: ctx[1] },
    {
      "stroke-width": svg_stroke_width_value = ctx[4] ? Number(ctx[3]) * 24 / Number(ctx[2]) : ctx[3]
    },
    {
      class: svg_class_value = `lucide-icon lucide lucide-${ctx[0]} ${(_a = ctx[7].class) != null ? _a : ""}`
    }
  ];
  let svg_data = {};
  for (let i = 0; i < svg_levels.length; i += 1) {
    svg_data = assign(svg_data, svg_levels[i]);
  }
  return {
    c() {
      svg = svg_element("svg");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      each_1_anchor = empty();
      if (default_slot)
        default_slot.c();
      set_svg_attributes(svg, svg_data);
    },
    m(target, anchor) {
      insert(target, svg, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(svg, null);
        }
      }
      append(svg, each_1_anchor);
      if (default_slot) {
        default_slot.m(svg, null);
      }
      current = true;
    },
    p(ctx2, [dirty]) {
      var _a2;
      if (dirty & 32) {
        each_value = ctx2[5];
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context$4(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block$4(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(svg, each_1_anchor);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value.length;
      }
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 256)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[8],
            !current ? get_all_dirty_from_scope(ctx2[8]) : get_slot_changes(default_slot_template, ctx2[8], dirty, null),
            null
          );
        }
      }
      set_svg_attributes(svg, svg_data = get_spread_update(svg_levels, [
        defaultAttributes$1,
        dirty & 64 && ctx2[6],
        (!current || dirty & 4) && { width: ctx2[2] },
        (!current || dirty & 4) && { height: ctx2[2] },
        (!current || dirty & 2) && { stroke: ctx2[1] },
        (!current || dirty & 28 && svg_stroke_width_value !== (svg_stroke_width_value = ctx2[4] ? Number(ctx2[3]) * 24 / Number(ctx2[2]) : ctx2[3])) && { "stroke-width": svg_stroke_width_value },
        (!current || dirty & 129 && svg_class_value !== (svg_class_value = `lucide-icon lucide lucide-${ctx2[0]} ${(_a2 = ctx2[7].class) != null ? _a2 : ""}`)) && { class: svg_class_value }
      ]));
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (detaching)
        detach(svg);
      destroy_each(each_blocks, detaching);
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function instance$h($$self, $$props, $$invalidate) {
  const omit_props_names = ["name", "color", "size", "strokeWidth", "absoluteStrokeWidth", "iconNode"];
  let $$restProps = compute_rest_props($$props, omit_props_names);
  let { $$slots: slots = {}, $$scope } = $$props;
  let { name } = $$props;
  let { color = "currentColor" } = $$props;
  let { size = 24 } = $$props;
  let { strokeWidth = 2 } = $$props;
  let { absoluteStrokeWidth = false } = $$props;
  let { iconNode } = $$props;
  $$self.$$set = ($$new_props) => {
    $$invalidate(7, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    $$invalidate(6, $$restProps = compute_rest_props($$props, omit_props_names));
    if ("name" in $$new_props)
      $$invalidate(0, name = $$new_props.name);
    if ("color" in $$new_props)
      $$invalidate(1, color = $$new_props.color);
    if ("size" in $$new_props)
      $$invalidate(2, size = $$new_props.size);
    if ("strokeWidth" in $$new_props)
      $$invalidate(3, strokeWidth = $$new_props.strokeWidth);
    if ("absoluteStrokeWidth" in $$new_props)
      $$invalidate(4, absoluteStrokeWidth = $$new_props.absoluteStrokeWidth);
    if ("iconNode" in $$new_props)
      $$invalidate(5, iconNode = $$new_props.iconNode);
    if ("$$scope" in $$new_props)
      $$invalidate(8, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [
    name,
    color,
    size,
    strokeWidth,
    absoluteStrokeWidth,
    iconNode,
    $$restProps,
    $$props,
    $$scope,
    slots
  ];
}
class Icon extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$h, create_fragment$h, safe_not_equal, {
      name: 0,
      color: 1,
      size: 2,
      strokeWidth: 3,
      absoluteStrokeWidth: 4,
      iconNode: 5
    });
  }
}
const Icon$1 = Icon;
function create_default_slot$9(ctx) {
  let current;
  const default_slot_template = ctx[2].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[3], null);
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 8)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[3],
            !current ? get_all_dirty_from_scope(ctx2[3]) : get_slot_changes(default_slot_template, ctx2[3], dirty, null),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_fragment$g(ctx) {
  let icon;
  let current;
  const icon_spread_levels = [
    { name: "arrow-down-from-line" },
    ctx[1],
    { iconNode: ctx[0] }
  ];
  let icon_props = {
    $$slots: { default: [create_default_slot$9] },
    $$scope: { ctx }
  };
  for (let i = 0; i < icon_spread_levels.length; i += 1) {
    icon_props = assign(icon_props, icon_spread_levels[i]);
  }
  icon = new Icon$1({ props: icon_props });
  return {
    c() {
      create_component(icon.$$.fragment);
    },
    m(target, anchor) {
      mount_component(icon, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const icon_changes = dirty & 3 ? get_spread_update(icon_spread_levels, [
        icon_spread_levels[0],
        dirty & 2 && get_spread_object(ctx2[1]),
        dirty & 1 && { iconNode: ctx2[0] }
      ]) : {};
      if (dirty & 8) {
        icon_changes.$$scope = { dirty, ctx: ctx2 };
      }
      icon.$set(icon_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(icon.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(icon.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(icon, detaching);
    }
  };
}
function instance$g($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const iconNode = [
    ["path", { "d": "M19 3H5" }],
    ["path", { "d": "M12 21V7" }],
    ["path", { "d": "m6 15 6 6 6-6" }]
  ];
  $$self.$$set = ($$new_props) => {
    $$invalidate(1, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    if ("$$scope" in $$new_props)
      $$invalidate(3, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [iconNode, $$props, slots, $$scope];
}
class Arrow_down_from_line extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$g, create_fragment$g, safe_not_equal, {});
  }
}
const ArrowDownFromLine = Arrow_down_from_line;
function create_default_slot$8(ctx) {
  let current;
  const default_slot_template = ctx[2].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[3], null);
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 8)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[3],
            !current ? get_all_dirty_from_scope(ctx2[3]) : get_slot_changes(default_slot_template, ctx2[3], dirty, null),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_fragment$f(ctx) {
  let icon;
  let current;
  const icon_spread_levels = [
    { name: "arrow-up-from-line" },
    ctx[1],
    { iconNode: ctx[0] }
  ];
  let icon_props = {
    $$slots: { default: [create_default_slot$8] },
    $$scope: { ctx }
  };
  for (let i = 0; i < icon_spread_levels.length; i += 1) {
    icon_props = assign(icon_props, icon_spread_levels[i]);
  }
  icon = new Icon$1({ props: icon_props });
  return {
    c() {
      create_component(icon.$$.fragment);
    },
    m(target, anchor) {
      mount_component(icon, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const icon_changes = dirty & 3 ? get_spread_update(icon_spread_levels, [
        icon_spread_levels[0],
        dirty & 2 && get_spread_object(ctx2[1]),
        dirty & 1 && { iconNode: ctx2[0] }
      ]) : {};
      if (dirty & 8) {
        icon_changes.$$scope = { dirty, ctx: ctx2 };
      }
      icon.$set(icon_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(icon.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(icon.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(icon, detaching);
    }
  };
}
function instance$f($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const iconNode = [
    ["path", { "d": "m18 9-6-6-6 6" }],
    ["path", { "d": "M12 3v14" }],
    ["path", { "d": "M5 21h14" }]
  ];
  $$self.$$set = ($$new_props) => {
    $$invalidate(1, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    if ("$$scope" in $$new_props)
      $$invalidate(3, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [iconNode, $$props, slots, $$scope];
}
class Arrow_up_from_line extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$f, create_fragment$f, safe_not_equal, {});
  }
}
const ArrowUpFromLine = Arrow_up_from_line;
function create_default_slot$7(ctx) {
  let current;
  const default_slot_template = ctx[2].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[3], null);
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 8)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[3],
            !current ? get_all_dirty_from_scope(ctx2[3]) : get_slot_changes(default_slot_template, ctx2[3], dirty, null),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_fragment$e(ctx) {
  let icon;
  let current;
  const icon_spread_levels = [
    { name: "minus-square" },
    ctx[1],
    { iconNode: ctx[0] }
  ];
  let icon_props = {
    $$slots: { default: [create_default_slot$7] },
    $$scope: { ctx }
  };
  for (let i = 0; i < icon_spread_levels.length; i += 1) {
    icon_props = assign(icon_props, icon_spread_levels[i]);
  }
  icon = new Icon$1({ props: icon_props });
  return {
    c() {
      create_component(icon.$$.fragment);
    },
    m(target, anchor) {
      mount_component(icon, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const icon_changes = dirty & 3 ? get_spread_update(icon_spread_levels, [
        icon_spread_levels[0],
        dirty & 2 && get_spread_object(ctx2[1]),
        dirty & 1 && { iconNode: ctx2[0] }
      ]) : {};
      if (dirty & 8) {
        icon_changes.$$scope = { dirty, ctx: ctx2 };
      }
      icon.$set(icon_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(icon.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(icon.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(icon, detaching);
    }
  };
}
function instance$e($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const iconNode = [
    [
      "rect",
      {
        "width": "18",
        "height": "18",
        "x": "3",
        "y": "3",
        "rx": "2"
      }
    ],
    ["path", { "d": "M8 12h8" }]
  ];
  $$self.$$set = ($$new_props) => {
    $$invalidate(1, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    if ("$$scope" in $$new_props)
      $$invalidate(3, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [iconNode, $$props, slots, $$scope];
}
class Minus_square extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$e, create_fragment$e, safe_not_equal, {});
  }
}
const MinusSquare = Minus_square;
function create_default_slot$6(ctx) {
  let current;
  const default_slot_template = ctx[2].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[3], null);
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 8)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[3],
            !current ? get_all_dirty_from_scope(ctx2[3]) : get_slot_changes(default_slot_template, ctx2[3], dirty, null),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_fragment$d(ctx) {
  let icon;
  let current;
  const icon_spread_levels = [{ name: "pause" }, ctx[1], { iconNode: ctx[0] }];
  let icon_props = {
    $$slots: { default: [create_default_slot$6] },
    $$scope: { ctx }
  };
  for (let i = 0; i < icon_spread_levels.length; i += 1) {
    icon_props = assign(icon_props, icon_spread_levels[i]);
  }
  icon = new Icon$1({ props: icon_props });
  return {
    c() {
      create_component(icon.$$.fragment);
    },
    m(target, anchor) {
      mount_component(icon, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const icon_changes = dirty & 3 ? get_spread_update(icon_spread_levels, [
        icon_spread_levels[0],
        dirty & 2 && get_spread_object(ctx2[1]),
        dirty & 1 && { iconNode: ctx2[0] }
      ]) : {};
      if (dirty & 8) {
        icon_changes.$$scope = { dirty, ctx: ctx2 };
      }
      icon.$set(icon_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(icon.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(icon.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(icon, detaching);
    }
  };
}
function instance$d($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const iconNode = [
    [
      "rect",
      {
        "width": "4",
        "height": "16",
        "x": "6",
        "y": "4"
      }
    ],
    [
      "rect",
      {
        "width": "4",
        "height": "16",
        "x": "14",
        "y": "4"
      }
    ]
  ];
  $$self.$$set = ($$new_props) => {
    $$invalidate(1, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    if ("$$scope" in $$new_props)
      $$invalidate(3, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [iconNode, $$props, slots, $$scope];
}
class Pause extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$d, create_fragment$d, safe_not_equal, {});
  }
}
const Pause$1 = Pause;
function create_default_slot$5(ctx) {
  let current;
  const default_slot_template = ctx[2].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[3], null);
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 8)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[3],
            !current ? get_all_dirty_from_scope(ctx2[3]) : get_slot_changes(default_slot_template, ctx2[3], dirty, null),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_fragment$c(ctx) {
  let icon;
  let current;
  const icon_spread_levels = [{ name: "pie-chart" }, ctx[1], { iconNode: ctx[0] }];
  let icon_props = {
    $$slots: { default: [create_default_slot$5] },
    $$scope: { ctx }
  };
  for (let i = 0; i < icon_spread_levels.length; i += 1) {
    icon_props = assign(icon_props, icon_spread_levels[i]);
  }
  icon = new Icon$1({ props: icon_props });
  return {
    c() {
      create_component(icon.$$.fragment);
    },
    m(target, anchor) {
      mount_component(icon, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const icon_changes = dirty & 3 ? get_spread_update(icon_spread_levels, [
        icon_spread_levels[0],
        dirty & 2 && get_spread_object(ctx2[1]),
        dirty & 1 && { iconNode: ctx2[0] }
      ]) : {};
      if (dirty & 8) {
        icon_changes.$$scope = { dirty, ctx: ctx2 };
      }
      icon.$set(icon_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(icon.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(icon.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(icon, detaching);
    }
  };
}
function instance$c($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const iconNode = [
    ["path", { "d": "M21.21 15.89A10 10 0 1 1 8 2.83" }],
    ["path", { "d": "M22 12A10 10 0 0 0 12 2v10z" }]
  ];
  $$self.$$set = ($$new_props) => {
    $$invalidate(1, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    if ("$$scope" in $$new_props)
      $$invalidate(3, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [iconNode, $$props, slots, $$scope];
}
class Pie_chart extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$c, create_fragment$c, safe_not_equal, {});
  }
}
const PieChart = Pie_chart;
function create_default_slot$4(ctx) {
  let current;
  const default_slot_template = ctx[2].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[3], null);
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 8)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[3],
            !current ? get_all_dirty_from_scope(ctx2[3]) : get_slot_changes(default_slot_template, ctx2[3], dirty, null),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_fragment$b(ctx) {
  let icon;
  let current;
  const icon_spread_levels = [{ name: "play" }, ctx[1], { iconNode: ctx[0] }];
  let icon_props = {
    $$slots: { default: [create_default_slot$4] },
    $$scope: { ctx }
  };
  for (let i = 0; i < icon_spread_levels.length; i += 1) {
    icon_props = assign(icon_props, icon_spread_levels[i]);
  }
  icon = new Icon$1({ props: icon_props });
  return {
    c() {
      create_component(icon.$$.fragment);
    },
    m(target, anchor) {
      mount_component(icon, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const icon_changes = dirty & 3 ? get_spread_update(icon_spread_levels, [
        icon_spread_levels[0],
        dirty & 2 && get_spread_object(ctx2[1]),
        dirty & 1 && { iconNode: ctx2[0] }
      ]) : {};
      if (dirty & 8) {
        icon_changes.$$scope = { dirty, ctx: ctx2 };
      }
      icon.$set(icon_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(icon.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(icon.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(icon, detaching);
    }
  };
}
function instance$b($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const iconNode = [["polygon", { "points": "5 3 19 12 5 21 5 3" }]];
  $$self.$$set = ($$new_props) => {
    $$invalidate(1, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    if ("$$scope" in $$new_props)
      $$invalidate(3, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [iconNode, $$props, slots, $$scope];
}
class Play extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$b, create_fragment$b, safe_not_equal, {});
  }
}
const Play$1 = Play;
function create_default_slot$3(ctx) {
  let current;
  const default_slot_template = ctx[2].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[3], null);
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 8)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[3],
            !current ? get_all_dirty_from_scope(ctx2[3]) : get_slot_changes(default_slot_template, ctx2[3], dirty, null),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_fragment$a(ctx) {
  let icon;
  let current;
  const icon_spread_levels = [{ name: "plus-square" }, ctx[1], { iconNode: ctx[0] }];
  let icon_props = {
    $$slots: { default: [create_default_slot$3] },
    $$scope: { ctx }
  };
  for (let i = 0; i < icon_spread_levels.length; i += 1) {
    icon_props = assign(icon_props, icon_spread_levels[i]);
  }
  icon = new Icon$1({ props: icon_props });
  return {
    c() {
      create_component(icon.$$.fragment);
    },
    m(target, anchor) {
      mount_component(icon, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const icon_changes = dirty & 3 ? get_spread_update(icon_spread_levels, [
        icon_spread_levels[0],
        dirty & 2 && get_spread_object(ctx2[1]),
        dirty & 1 && { iconNode: ctx2[0] }
      ]) : {};
      if (dirty & 8) {
        icon_changes.$$scope = { dirty, ctx: ctx2 };
      }
      icon.$set(icon_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(icon.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(icon.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(icon, detaching);
    }
  };
}
function instance$a($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const iconNode = [
    [
      "rect",
      {
        "width": "18",
        "height": "18",
        "x": "3",
        "y": "3",
        "rx": "2"
      }
    ],
    ["path", { "d": "M8 12h8" }],
    ["path", { "d": "M12 8v8" }]
  ];
  $$self.$$set = ($$new_props) => {
    $$invalidate(1, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    if ("$$scope" in $$new_props)
      $$invalidate(3, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [iconNode, $$props, slots, $$scope];
}
class Plus_square extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$a, create_fragment$a, safe_not_equal, {});
  }
}
const PlusSquare = Plus_square;
function create_default_slot$2(ctx) {
  let current;
  const default_slot_template = ctx[2].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[3], null);
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 8)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[3],
            !current ? get_all_dirty_from_scope(ctx2[3]) : get_slot_changes(default_slot_template, ctx2[3], dirty, null),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_fragment$9(ctx) {
  let icon;
  let current;
  const icon_spread_levels = [{ name: "refresh-ccw" }, ctx[1], { iconNode: ctx[0] }];
  let icon_props = {
    $$slots: { default: [create_default_slot$2] },
    $$scope: { ctx }
  };
  for (let i = 0; i < icon_spread_levels.length; i += 1) {
    icon_props = assign(icon_props, icon_spread_levels[i]);
  }
  icon = new Icon$1({ props: icon_props });
  return {
    c() {
      create_component(icon.$$.fragment);
    },
    m(target, anchor) {
      mount_component(icon, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const icon_changes = dirty & 3 ? get_spread_update(icon_spread_levels, [
        icon_spread_levels[0],
        dirty & 2 && get_spread_object(ctx2[1]),
        dirty & 1 && { iconNode: ctx2[0] }
      ]) : {};
      if (dirty & 8) {
        icon_changes.$$scope = { dirty, ctx: ctx2 };
      }
      icon.$set(icon_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(icon.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(icon.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(icon, detaching);
    }
  };
}
function instance$9($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const iconNode = [
    [
      "path",
      {
        "d": "M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"
      }
    ],
    ["path", { "d": "M3 3v5h5" }],
    [
      "path",
      {
        "d": "M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"
      }
    ],
    ["path", { "d": "M16 16h5v5" }]
  ];
  $$self.$$set = ($$new_props) => {
    $$invalidate(1, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    if ("$$scope" in $$new_props)
      $$invalidate(3, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [iconNode, $$props, slots, $$scope];
}
class Refresh_ccw extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$9, create_fragment$9, safe_not_equal, {});
  }
}
const RefreshCcw = Refresh_ccw;
function create_default_slot$1(ctx) {
  let current;
  const default_slot_template = ctx[2].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[3], null);
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 8)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[3],
            !current ? get_all_dirty_from_scope(ctx2[3]) : get_slot_changes(default_slot_template, ctx2[3], dirty, null),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_fragment$8(ctx) {
  let icon;
  let current;
  const icon_spread_levels = [{ name: "timer" }, ctx[1], { iconNode: ctx[0] }];
  let icon_props = {
    $$slots: { default: [create_default_slot$1] },
    $$scope: { ctx }
  };
  for (let i = 0; i < icon_spread_levels.length; i += 1) {
    icon_props = assign(icon_props, icon_spread_levels[i]);
  }
  icon = new Icon$1({ props: icon_props });
  return {
    c() {
      create_component(icon.$$.fragment);
    },
    m(target, anchor) {
      mount_component(icon, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const icon_changes = dirty & 3 ? get_spread_update(icon_spread_levels, [
        icon_spread_levels[0],
        dirty & 2 && get_spread_object(ctx2[1]),
        dirty & 1 && { iconNode: ctx2[0] }
      ]) : {};
      if (dirty & 8) {
        icon_changes.$$scope = { dirty, ctx: ctx2 };
      }
      icon.$set(icon_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(icon.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(icon.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(icon, detaching);
    }
  };
}
function instance$8($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const iconNode = [
    [
      "line",
      {
        "x1": "10",
        "x2": "14",
        "y1": "2",
        "y2": "2"
      }
    ],
    [
      "line",
      {
        "x1": "12",
        "x2": "15",
        "y1": "14",
        "y2": "11"
      }
    ],
    ["circle", { "cx": "12", "cy": "14", "r": "8" }]
  ];
  $$self.$$set = ($$new_props) => {
    $$invalidate(1, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    if ("$$scope" in $$new_props)
      $$invalidate(3, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [iconNode, $$props, slots, $$scope];
}
class Timer extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$8, create_fragment$8, safe_not_equal, {});
  }
}
const Timer$1 = Timer;
function create_default_slot(ctx) {
  let current;
  const default_slot_template = ctx[2].default;
  const default_slot = create_slot(default_slot_template, ctx, ctx[3], null);
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & 8)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            ctx2[3],
            !current ? get_all_dirty_from_scope(ctx2[3]) : get_slot_changes(default_slot_template, ctx2[3], dirty, null),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_fragment$7(ctx) {
  let icon;
  let current;
  const icon_spread_levels = [{ name: "trash-2" }, ctx[1], { iconNode: ctx[0] }];
  let icon_props = {
    $$slots: { default: [create_default_slot] },
    $$scope: { ctx }
  };
  for (let i = 0; i < icon_spread_levels.length; i += 1) {
    icon_props = assign(icon_props, icon_spread_levels[i]);
  }
  icon = new Icon$1({ props: icon_props });
  return {
    c() {
      create_component(icon.$$.fragment);
    },
    m(target, anchor) {
      mount_component(icon, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const icon_changes = dirty & 3 ? get_spread_update(icon_spread_levels, [
        icon_spread_levels[0],
        dirty & 2 && get_spread_object(ctx2[1]),
        dirty & 1 && { iconNode: ctx2[0] }
      ]) : {};
      if (dirty & 8) {
        icon_changes.$$scope = { dirty, ctx: ctx2 };
      }
      icon.$set(icon_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(icon.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(icon.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(icon, detaching);
    }
  };
}
function instance$7($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const iconNode = [
    ["path", { "d": "M3 6h18" }],
    [
      "path",
      {
        "d": "M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"
      }
    ],
    [
      "path",
      {
        "d": "M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"
      }
    ],
    [
      "line",
      {
        "x1": "10",
        "x2": "10",
        "y1": "11",
        "y2": "17"
      }
    ],
    [
      "line",
      {
        "x1": "14",
        "x2": "14",
        "y1": "11",
        "y2": "17"
      }
    ]
  ];
  $$self.$$set = ($$new_props) => {
    $$invalidate(1, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
    if ("$$scope" in $$new_props)
      $$invalidate(3, $$scope = $$new_props.$$scope);
  };
  $$props = exclude_internal_props($$props);
  return [iconNode, $$props, slots, $$scope];
}
class Trash_2 extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$7, create_fragment$7, safe_not_equal, {});
  }
}
const Trash2 = Trash_2;
function fade(node, { delay = 0, duration = 400, easing = identity } = {}) {
  const o = +getComputedStyle(node).opacity;
  return {
    delay,
    duration,
    easing,
    css: (t) => `opacity: ${t * o}`
  };
}
function ifClickEquivalent(fn) {
  return (e) => {
    if (["Enter", " "].contains(e.key)) {
      fn(e);
      e.preventDefault();
    }
  };
}
function create_else_block$3(ctx) {
  let input;
  let mounted;
  let dispose;
  return {
    c() {
      input = element("input");
      attr(input, "type", "text");
    },
    m(target, anchor) {
      insert(target, input, anchor);
      set_input_value(input, ctx[2]);
      if (!mounted) {
        dispose = [
          listen(input, "input", ctx[7]),
          action_destroyer(takeFocus$1.call(null, input)),
          listen(input, "keydown", ctx[5])
        ];
        mounted = true;
      }
    },
    p(ctx2, dirty) {
      if (dirty & 4 && input.value !== ctx2[2]) {
        set_input_value(input, ctx2[2]);
      }
    },
    d(detaching) {
      if (detaching)
        detach(input);
      mounted = false;
      run_all(dispose);
    }
  };
}
function create_if_block$5(ctx) {
  let span;
  let t0;
  let t1;
  let mounted;
  let dispose;
  let if_block = ctx[1] == "" && create_if_block_1$4();
  return {
    c() {
      span = element("span");
      if (if_block)
        if_block.c();
      t0 = space();
      t1 = text(ctx[1]);
      attr(span, "role", "button");
      attr(span, "tabindex", "0");
    },
    m(target, anchor) {
      insert(target, span, anchor);
      if (if_block)
        if_block.m(span, null);
      append(span, t0);
      append(span, t1);
      ctx[6](span);
      if (!mounted) {
        dispose = [
          listen(span, "click", ctx[4]),
          listen(span, "keydown", ifClickEquivalent(ctx[4]))
        ];
        mounted = true;
      }
    },
    p(ctx2, dirty) {
      if (ctx2[1] == "") {
        if (if_block)
          ;
        else {
          if_block = create_if_block_1$4();
          if_block.c();
          if_block.m(span, t0);
        }
      } else if (if_block) {
        if_block.d(1);
        if_block = null;
      }
      if (dirty & 2)
        set_data(t1, ctx2[1]);
    },
    d(detaching) {
      if (detaching)
        detach(span);
      if (if_block)
        if_block.d();
      ctx[6](null);
      mounted = false;
      run_all(dispose);
    }
  };
}
function create_if_block_1$4(ctx) {
  let t;
  return {
    c() {
      t = text("\xA0");
    },
    m(target, anchor) {
      insert(target, t, anchor);
    },
    d(detaching) {
      if (detaching)
        detach(t);
    }
  };
}
function create_fragment$6(ctx) {
  let if_block_anchor;
  function select_block_type(ctx2, dirty) {
    if (ctx2[0] === EditMode$1.Read)
      return create_if_block$5;
    return create_else_block$3;
  }
  let current_block_type = select_block_type(ctx);
  let if_block = current_block_type(ctx);
  return {
    c() {
      if_block.c();
      if_block_anchor = empty();
    },
    m(target, anchor) {
      if_block.m(target, anchor);
      insert(target, if_block_anchor, anchor);
    },
    p(ctx2, [dirty]) {
      if (current_block_type === (current_block_type = select_block_type(ctx2)) && if_block) {
        if_block.p(ctx2, dirty);
      } else {
        if_block.d(1);
        if_block = current_block_type(ctx2);
        if (if_block) {
          if_block.c();
          if_block.m(if_block_anchor.parentNode, if_block_anchor);
        }
      }
    },
    i: noop,
    o: noop,
    d(detaching) {
      if_block.d(detaching);
      if (detaching)
        detach(if_block_anchor);
    }
  };
}
var EditMode$1;
(function(EditMode2) {
  EditMode2[EditMode2["Read"] = 0] = "Read";
  EditMode2[EditMode2["Edit"] = 1] = "Edit";
})(EditMode$1 || (EditMode$1 = {}));
function takeFocus$1(el) {
  el.focus();
  el.select();
}
function instance$6($$self, $$props, $$invalidate) {
  const dispatch2 = createEventDispatcher();
  let { value = "" } = $$props;
  let newValue = value;
  let focusTarget;
  let { mode = EditMode$1.Read } = $$props;
  function startEditing() {
    $$invalidate(0, mode = EditMode$1.Edit);
  }
  function onKeyDown(e) {
    if (e.key === "Enter") {
      $$invalidate(1, value = $$invalidate(2, newValue = newValue.trim()));
      $$invalidate(0, mode = EditMode$1.Read);
      dispatch2("confirmed", { value });
    } else if (e.key === "Escape") {
      $$invalidate(2, newValue = value);
      $$invalidate(0, mode = EditMode$1.Read);
      dispatch2("cancelled", { value });
    }
    tick().then(() => focusTarget === null || focusTarget === void 0 ? void 0 : focusTarget.focus());
  }
  function span_binding($$value) {
    binding_callbacks[$$value ? "unshift" : "push"](() => {
      focusTarget = $$value;
      $$invalidate(3, focusTarget);
    });
  }
  function input_input_handler() {
    newValue = this.value;
    $$invalidate(2, newValue);
  }
  $$self.$$set = ($$props2) => {
    if ("value" in $$props2)
      $$invalidate(1, value = $$props2.value);
    if ("mode" in $$props2)
      $$invalidate(0, mode = $$props2.mode);
  };
  $$self.$$.update = () => {
    if ($$self.$$.dirty & 1) {
      dispatch2("modeChanged", { mode });
    }
  };
  return [
    mode,
    value,
    newValue,
    focusTarget,
    startEditing,
    onKeyDown,
    span_binding,
    input_input_handler
  ];
}
class EditableText extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$6, create_fragment$6, safe_not_equal, { value: 1, mode: 0 });
  }
}
function create_else_block$2(ctx) {
  let input;
  let mounted;
  let dispose;
  return {
    c() {
      input = element("input");
      attr(input, "type", "text");
    },
    m(target, anchor) {
      insert(target, input, anchor);
      set_input_value(input, ctx[2]);
      if (!mounted) {
        dispose = [
          listen(input, "input", ctx[8]),
          action_destroyer(takeFocus.call(null, input)),
          listen(input, "keydown", ctx[5])
        ];
        mounted = true;
      }
    },
    p(ctx2, dirty) {
      if (dirty & 4 && input.value !== ctx2[2]) {
        set_input_value(input, ctx2[2]);
      }
    },
    d(detaching) {
      if (detaching)
        detach(input);
      mounted = false;
      run_all(dispose);
    }
  };
}
function create_if_block$4(ctx) {
  let span;
  let t;
  let mounted;
  let dispose;
  return {
    c() {
      span = element("span");
      t = text(ctx[1]);
      attr(span, "role", "button");
      attr(span, "tabindex", "0");
    },
    m(target, anchor) {
      insert(target, span, anchor);
      append(span, t);
      ctx[7](span);
      if (!mounted) {
        dispose = [
          listen(span, "click", prevent_default(ctx[4])),
          listen(span, "keydown", ctx[6])
        ];
        mounted = true;
      }
    },
    p(ctx2, dirty) {
      if (dirty & 2)
        set_data(t, ctx2[1]);
    },
    d(detaching) {
      if (detaching)
        detach(span);
      ctx[7](null);
      mounted = false;
      run_all(dispose);
    }
  };
}
function create_fragment$5(ctx) {
  let if_block_anchor;
  function select_block_type(ctx2, dirty) {
    if (ctx2[0] === EditMode.Read)
      return create_if_block$4;
    return create_else_block$2;
  }
  let current_block_type = select_block_type(ctx);
  let if_block = current_block_type(ctx);
  return {
    c() {
      if_block.c();
      if_block_anchor = empty();
    },
    m(target, anchor) {
      if_block.m(target, anchor);
      insert(target, if_block_anchor, anchor);
    },
    p(ctx2, [dirty]) {
      if (current_block_type === (current_block_type = select_block_type(ctx2)) && if_block) {
        if_block.p(ctx2, dirty);
      } else {
        if_block.d(1);
        if_block = current_block_type(ctx2);
        if (if_block) {
          if_block.c();
          if_block.m(if_block_anchor.parentNode, if_block_anchor);
        }
      }
    },
    i: noop,
    o: noop,
    d(detaching) {
      if_block.d(detaching);
      if (detaching)
        detach(if_block_anchor);
    }
  };
}
var EditMode;
(function(EditMode2) {
  EditMode2[EditMode2["Read"] = 0] = "Read";
  EditMode2[EditMode2["Edit"] = 1] = "Edit";
})(EditMode || (EditMode = {}));
function takeFocus(el) {
  el.focus();
  el.select();
}
function instance$5($$self, $$props, $$invalidate) {
  const dispatch2 = createEventDispatcher();
  let { value = 0 } = $$props;
  let newValue = value.toString();
  let focusTarget;
  let { mode = EditMode.Read } = $$props;
  function startEditing() {
    if (!newValue.startsWith("+") && !newValue.startsWith("-")) {
      $$invalidate(2, newValue = value.toString());
    }
    $$invalidate(0, mode = EditMode.Edit);
  }
  function onEditKeyDown(e) {
    if (e.key === "Enter") {
      $$invalidate(2, newValue = newValue.trim());
      if (newValue.startsWith("+") || newValue.startsWith("-")) {
        $$invalidate(1, value += Number(newValue));
      } else {
        $$invalidate(1, value = Number(newValue));
      }
      $$invalidate(0, mode = EditMode.Read);
      dispatch2("confirmed", { value });
    } else if (e.key === "Escape") {
      $$invalidate(0, mode = EditMode.Read);
      dispatch2("cancelled", { value });
    }
    tick().then(() => focusTarget === null || focusTarget === void 0 ? void 0 : focusTarget.focus());
  }
  function onSpanKeyDown(e) {
    if (["Enter", " "].contains(e.key)) {
      startEditing();
      e.preventDefault();
    } else if (["ArrowUp", "ArrowRight"].contains(e.key)) {
      $$invalidate(1, value += 1);
      e.preventDefault();
    } else if (["ArrowDown", "ArrowLeft"].contains(e.key)) {
      $$invalidate(1, value -= 1);
      e.preventDefault();
    }
  }
  function span_binding($$value) {
    binding_callbacks[$$value ? "unshift" : "push"](() => {
      focusTarget = $$value;
      $$invalidate(3, focusTarget);
    });
  }
  function input_input_handler() {
    newValue = this.value;
    $$invalidate(2, newValue);
  }
  $$self.$$set = ($$props2) => {
    if ("value" in $$props2)
      $$invalidate(1, value = $$props2.value);
    if ("mode" in $$props2)
      $$invalidate(0, mode = $$props2.mode);
  };
  $$self.$$.update = () => {
    if ($$self.$$.dirty & 1) {
      dispatch2("modeChanged", { mode });
    }
  };
  return [
    mode,
    value,
    newValue,
    focusTarget,
    startEditing,
    onEditKeyDown,
    onSpanKeyDown,
    span_binding,
    input_input_handler
  ];
}
class EditableNumber extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$5, create_fragment$5, safe_not_equal, { value: 1, mode: 0 });
  }
}
function get_each_context$3(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[14] = list[i].x1;
  child_ctx[15] = list[i].x2;
  child_ctx[16] = list[i].y1;
  child_ctx[17] = list[i].y2;
  child_ctx[18] = list[i].isFilled;
  child_ctx[20] = i;
  return child_ctx;
}
function create_if_block_1$3(ctx) {
  let each_1_anchor;
  let each_value = ctx[4](ctx[0], ctx[1]);
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block$3(get_each_context$3(ctx, each_value, i));
  }
  return {
    c() {
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      each_1_anchor = empty();
    },
    m(target, anchor) {
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(target, anchor);
        }
      }
      insert(target, each_1_anchor, anchor);
    },
    p(ctx2, dirty) {
      if (dirty & 19) {
        each_value = ctx2[4](ctx2[0], ctx2[1]);
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context$3(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block$3(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(each_1_anchor.parentNode, each_1_anchor);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value.length;
      }
    },
    d(detaching) {
      destroy_each(each_blocks, detaching);
      if (detaching)
        detach(each_1_anchor);
    }
  };
}
function create_each_block$3(ctx) {
  let path;
  let path_data_filled_value;
  let path_d_value;
  return {
    c() {
      path = svg_element("path");
      attr(path, "data-segment", ctx[20]);
      attr(path, "data-filled", path_data_filled_value = ctx[18]);
      attr(path, "d", path_d_value = "\n        M " + (radius + padding) + " " + (radius + padding) + "\n        L " + ctx[14] + " " + ctx[16] + "\n        A " + radius + " " + radius + " 0 0 1 " + ctx[15] + " " + ctx[17] + "\n        Z");
    },
    m(target, anchor) {
      insert(target, path, anchor);
    },
    p(ctx2, dirty) {
      if (dirty & 3 && path_data_filled_value !== (path_data_filled_value = ctx2[18])) {
        attr(path, "data-filled", path_data_filled_value);
      }
      if (dirty & 3 && path_d_value !== (path_d_value = "\n        M " + (radius + padding) + " " + (radius + padding) + "\n        L " + ctx2[14] + " " + ctx2[16] + "\n        A " + radius + " " + radius + " 0 0 1 " + ctx2[15] + " " + ctx2[17] + "\n        Z")) {
        attr(path, "d", path_d_value);
      }
    },
    d(detaching) {
      if (detaching)
        detach(path);
    }
  };
}
function create_if_block$3(ctx) {
  let div;
  let button0;
  let minussquare;
  let t0;
  let button1;
  let plussquare;
  let t1;
  let button2;
  let arrowdownfromline;
  let t2;
  let button3;
  let arrowupfromline;
  let current;
  let mounted;
  let dispose;
  minussquare = new MinusSquare({});
  plussquare = new PlusSquare({});
  arrowdownfromline = new ArrowDownFromLine({});
  arrowupfromline = new ArrowUpFromLine({});
  return {
    c() {
      div = element("div");
      button0 = element("button");
      create_component(minussquare.$$.fragment);
      t0 = space();
      button1 = element("button");
      create_component(plussquare.$$.fragment);
      t1 = space();
      button2 = element("button");
      create_component(arrowdownfromline.$$.fragment);
      t2 = space();
      button3 = element("button");
      create_component(arrowupfromline.$$.fragment);
      attr(button0, "class", "progress-clocks-clock__decrement");
      attr(button0, "title", "Unfill one segment");
      attr(button1, "class", "progress-clocks-clock__increment");
      attr(button1, "title", "Fill one segment");
      attr(button2, "class", "progress-clocks-clock__decrement-segments");
      attr(button2, "title", "Remove one segment");
      attr(button3, "class", "progress-clocks-clock__increment-segments");
      attr(button3, "title", "Add another segment");
      attr(div, "class", "progress-clocks-clock__buttons");
    },
    m(target, anchor) {
      insert(target, div, anchor);
      append(div, button0);
      mount_component(minussquare, button0, null);
      append(div, t0);
      append(div, button1);
      mount_component(plussquare, button1, null);
      append(div, t1);
      append(div, button2);
      mount_component(arrowdownfromline, button2, null);
      append(div, t2);
      append(div, button3);
      mount_component(arrowupfromline, button3, null);
      current = true;
      if (!mounted) {
        dispose = [
          listen(button0, "click", prevent_default(ctx[6])),
          listen(button0, "keydown", ifClickEquivalent(ctx[6])),
          listen(button1, "click", prevent_default(ctx[5])),
          listen(button1, "keydown", ifClickEquivalent(ctx[5])),
          listen(button2, "click", prevent_default(ctx[9])),
          listen(button2, "keydown", function() {
            if (is_function(ifClickEquivalent(ctx[10])))
              ifClickEquivalent(ctx[10]).apply(this, arguments);
          }),
          listen(button3, "click", prevent_default(ctx[11])),
          listen(button3, "keydown", function() {
            if (is_function(ifClickEquivalent(ctx[12])))
              ifClickEquivalent(ctx[12]).apply(this, arguments);
          })
        ];
        mounted = true;
      }
    },
    p(new_ctx, dirty) {
      ctx = new_ctx;
    },
    i(local) {
      if (current)
        return;
      transition_in(minussquare.$$.fragment, local);
      transition_in(plussquare.$$.fragment, local);
      transition_in(arrowdownfromline.$$.fragment, local);
      transition_in(arrowupfromline.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(minussquare.$$.fragment, local);
      transition_out(plussquare.$$.fragment, local);
      transition_out(arrowdownfromline.$$.fragment, local);
      transition_out(arrowupfromline.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      if (detaching)
        detach(div);
      destroy_component(minussquare);
      destroy_component(plussquare);
      destroy_component(arrowdownfromline);
      destroy_component(arrowupfromline);
      mounted = false;
      run_all(dispose);
    }
  };
}
function create_fragment$4(ctx) {
  let div;
  let svg;
  let circle;
  let t;
  let current;
  let mounted;
  let dispose;
  let if_block0 = ctx[0] > 1 && create_if_block_1$3(ctx);
  let if_block1 = ctx[2] && create_if_block$3(ctx);
  return {
    c() {
      div = element("div");
      svg = svg_element("svg");
      if (if_block0)
        if_block0.c();
      circle = svg_element("circle");
      t = space();
      if (if_block1)
        if_block1.c();
      attr(circle, "cx", radius + padding);
      attr(circle, "cy", radius + padding);
      attr(circle, "r", radius);
      attr(circle, "data-filled", ctx[3]);
      attr(svg, "data-segments", ctx[0]);
      attr(svg, "data-filled", ctx[1]);
      attr(svg, "role", "button");
      attr(svg, "tabindex", "0");
      attr(svg, "xmlns", "http://www.w3.org/2000/svg");
      attr(svg, "viewBox", "0 0 " + (2 * radius + 2 * padding) + " " + (2 * radius + 2 * padding));
      attr(div, "class", "progress-clocks-clock");
    },
    m(target, anchor) {
      insert(target, div, anchor);
      append(div, svg);
      if (if_block0)
        if_block0.m(svg, null);
      append(svg, circle);
      append(div, t);
      if (if_block1)
        if_block1.m(div, null);
      current = true;
      if (!mounted) {
        dispose = [
          listen(svg, "click", prevent_default(ctx[5])),
          listen(svg, "contextmenu", prevent_default(ctx[6])),
          listen(svg, "keydown", ctx[7])
        ];
        mounted = true;
      }
    },
    p(ctx2, [dirty]) {
      if (ctx2[0] > 1) {
        if (if_block0) {
          if_block0.p(ctx2, dirty);
        } else {
          if_block0 = create_if_block_1$3(ctx2);
          if_block0.c();
          if_block0.m(svg, circle);
        }
      } else if (if_block0) {
        if_block0.d(1);
        if_block0 = null;
      }
      if (!current || dirty & 8) {
        attr(circle, "data-filled", ctx2[3]);
      }
      if (!current || dirty & 1) {
        attr(svg, "data-segments", ctx2[0]);
      }
      if (!current || dirty & 2) {
        attr(svg, "data-filled", ctx2[1]);
      }
      if (ctx2[2]) {
        if (if_block1) {
          if_block1.p(ctx2, dirty);
          if (dirty & 4) {
            transition_in(if_block1, 1);
          }
        } else {
          if_block1 = create_if_block$3(ctx2);
          if_block1.c();
          transition_in(if_block1, 1);
          if_block1.m(div, null);
        }
      } else if (if_block1) {
        group_outros();
        transition_out(if_block1, 1, 1, () => {
          if_block1 = null;
        });
        check_outros();
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(if_block1);
      current = true;
    },
    o(local) {
      transition_out(if_block1);
      current = false;
    },
    d(detaching) {
      if (detaching)
        detach(div);
      if (if_block0)
        if_block0.d();
      if (if_block1)
        if_block1.d();
      mounted = false;
      run_all(dispose);
    }
  };
}
const radius = 50;
const padding = 4;
function instance$4($$self, $$props, $$invalidate) {
  let fillCircle;
  let { segments = 4 } = $$props;
  let { filled = 0 } = $$props;
  let { showButtonsForInlineClocks = true } = $$props;
  let { allowClickInteractionForInlineClocks = true } = $$props;
  const dispatch2 = createEventDispatcher();
  function slices(segments2, filled2) {
    const ss = [];
    for (let i = 0; i < segments2; ++i) {
      const x1 = radius * Math.sin(2 * Math.PI * i / segments2) + radius + padding;
      const x2 = radius * Math.sin(2 * Math.PI * (i + 1) / segments2) + radius + padding;
      const y1 = -radius * Math.cos(2 * Math.PI * i / segments2) + radius + padding;
      const y2 = -radius * Math.cos(2 * Math.PI * (i + 1) / segments2) + radius + padding;
      ss.push({ x1, x2, y1, y2, isFilled: i < filled2 });
    }
    return ss;
  }
  function handleIncrement(e) {
    if (!allowClickInteractionForInlineClocks)
      return;
    if (e.ctrlKey || e.metaKey) {
      $$invalidate(0, segments += 1);
    } else {
      $$invalidate(1, filled += 1);
    }
  }
  function handleDecrement(e) {
    if (!allowClickInteractionForInlineClocks)
      return;
    if (e.ctrlKey || e.metaKey) {
      $$invalidate(0, segments -= 1);
      $$invalidate(1, filled = Math.min(segments, filled));
    } else {
      $$invalidate(1, filled -= 1);
    }
  }
  function handleClockKeyInteraction(e) {
    if (!allowClickInteractionForInlineClocks)
      return;
    if (["Enter", " ", "ArrowUp", "ArrowRight"].contains(e.key)) {
      if (e.ctrlKey || e.metaKey) {
        $$invalidate(0, segments += 1);
      } else {
        $$invalidate(1, filled += 1);
      }
      e.preventDefault();
    } else if (["ArrowDown", "ArrowLeft"].contains(e.key)) {
      if (e.ctrlKey || e.metaKey) {
        $$invalidate(0, segments -= 1);
        $$invalidate(1, filled = Math.min(segments, filled));
      } else {
        $$invalidate(1, filled -= 1);
      }
      e.preventDefault();
    }
  }
  const click_handler = () => $$invalidate(0, segments -= 1);
  const keydown_handler = () => $$invalidate(0, segments -= 1);
  const click_handler_1 = () => $$invalidate(0, segments += 1);
  const keydown_handler_1 = () => $$invalidate(0, segments += 1);
  $$self.$$set = ($$props2) => {
    if ("segments" in $$props2)
      $$invalidate(0, segments = $$props2.segments);
    if ("filled" in $$props2)
      $$invalidate(1, filled = $$props2.filled);
    if ("showButtonsForInlineClocks" in $$props2)
      $$invalidate(2, showButtonsForInlineClocks = $$props2.showButtonsForInlineClocks);
    if ("allowClickInteractionForInlineClocks" in $$props2)
      $$invalidate(8, allowClickInteractionForInlineClocks = $$props2.allowClickInteractionForInlineClocks);
  };
  $$self.$$.update = () => {
    if ($$self.$$.dirty & 1) {
      $$invalidate(0, segments = Math.max(1, segments));
    }
    if ($$self.$$.dirty & 3) {
      $$invalidate(1, filled = filled < 0 ? segments : filled);
    }
    if ($$self.$$.dirty & 3) {
      $$invalidate(1, filled = filled > segments ? 0 : filled);
    }
    if ($$self.$$.dirty & 3) {
      dispatch2("updated", { segments, filled });
    }
    if ($$self.$$.dirty & 3) {
      $$invalidate(3, fillCircle = segments <= 1 ? filled >= 1 : null);
    }
  };
  return [
    segments,
    filled,
    showButtonsForInlineClocks,
    fillCircle,
    slices,
    handleIncrement,
    handleDecrement,
    handleClockKeyInteraction,
    allowClickInteractionForInlineClocks,
    click_handler,
    keydown_handler,
    click_handler_1,
    keydown_handler_1
  ];
}
class Clock extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$4, create_fragment$4, safe_not_equal, {
      segments: 0,
      filled: 1,
      showButtonsForInlineClocks: 2,
      allowClickInteractionForInlineClocks: 8
    });
  }
}
function create_fragment$3(ctx) {
  let div4;
  let div0;
  let editablenumber;
  let updating_value;
  let t0;
  let div3;
  let div1;
  let minussquare;
  let t1;
  let div2;
  let plussquare;
  let current;
  let mounted;
  let dispose;
  function editablenumber_value_binding(value) {
    ctx[3](value);
  }
  let editablenumber_props = {};
  if (ctx[0] !== void 0) {
    editablenumber_props.value = ctx[0];
  }
  editablenumber = new EditableNumber({ props: editablenumber_props });
  binding_callbacks.push(() => bind(editablenumber, "value", editablenumber_value_binding));
  minussquare = new MinusSquare({});
  plussquare = new PlusSquare({});
  return {
    c() {
      div4 = element("div");
      div0 = element("div");
      create_component(editablenumber.$$.fragment);
      t0 = space();
      div3 = element("div");
      div1 = element("div");
      create_component(minussquare.$$.fragment);
      t1 = space();
      div2 = element("div");
      create_component(plussquare.$$.fragment);
      attr(div0, "class", "progress-clocks-counter__value");
      attr(div1, "role", "button");
      attr(div1, "tabindex", "0");
      attr(div1, "class", "progress-clocks-button progress-clocks-counter__decrement");
      attr(div2, "role", "button");
      attr(div2, "tabindex", "0");
      attr(div2, "class", "progress-clocks-button progress-clocks-counter__increment");
      attr(div3, "class", "progress-clocks-counter__buttons");
      attr(div4, "class", "progress-clocks-counter");
    },
    m(target, anchor) {
      insert(target, div4, anchor);
      append(div4, div0);
      mount_component(editablenumber, div0, null);
      append(div4, t0);
      append(div4, div3);
      append(div3, div1);
      mount_component(minussquare, div1, null);
      append(div3, t1);
      append(div3, div2);
      mount_component(plussquare, div2, null);
      current = true;
      if (!mounted) {
        dispose = [
          listen(div1, "click", prevent_default(ctx[2])),
          listen(div1, "keydown", ifClickEquivalent(ctx[2])),
          listen(div2, "click", prevent_default(ctx[1])),
          listen(div2, "keydown", ifClickEquivalent(ctx[1]))
        ];
        mounted = true;
      }
    },
    p(ctx2, [dirty]) {
      const editablenumber_changes = {};
      if (!updating_value && dirty & 1) {
        updating_value = true;
        editablenumber_changes.value = ctx2[0];
        add_flush_callback(() => updating_value = false);
      }
      editablenumber.$set(editablenumber_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(editablenumber.$$.fragment, local);
      transition_in(minussquare.$$.fragment, local);
      transition_in(plussquare.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(editablenumber.$$.fragment, local);
      transition_out(minussquare.$$.fragment, local);
      transition_out(plussquare.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      if (detaching)
        detach(div4);
      destroy_component(editablenumber);
      destroy_component(minussquare);
      destroy_component(plussquare);
      mounted = false;
      run_all(dispose);
    }
  };
}
function instance$3($$self, $$props, $$invalidate) {
  let { value = 0 } = $$props;
  const dispatch2 = createEventDispatcher();
  function increment() {
    $$invalidate(0, value += 1);
  }
  function decrement() {
    $$invalidate(0, value -= 1);
  }
  function editablenumber_value_binding(value$1) {
    value = value$1;
    $$invalidate(0, value);
  }
  $$self.$$set = ($$props2) => {
    if ("value" in $$props2)
      $$invalidate(0, value = $$props2.value);
  };
  $$self.$$.update = () => {
    if ($$self.$$.dirty & 1) {
      dispatch2("updated", { value });
    }
  };
  return [value, increment, decrement, editablenumber_value_binding];
}
class Counter extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$3, create_fragment$3, safe_not_equal, { value: 0, increment: 1, decrement: 2 });
  }
  get increment() {
    return this.$$.ctx[1];
  }
  get decrement() {
    return this.$$.ctx[2];
  }
}
function get_each_context$2(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[18] = list[i];
  child_ctx[20] = i;
  return child_ctx;
}
function create_else_block$1(ctx) {
  let play;
  let current;
  play = new Play$1({});
  return {
    c() {
      create_component(play.$$.fragment);
    },
    m(target, anchor) {
      mount_component(play, target, anchor);
      current = true;
    },
    i(local) {
      if (current)
        return;
      transition_in(play.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(play.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(play, detaching);
    }
  };
}
function create_if_block_1$2(ctx) {
  let pause;
  let current;
  pause = new Pause$1({});
  return {
    c() {
      create_component(pause.$$.fragment);
    },
    m(target, anchor) {
      mount_component(pause, target, anchor);
      current = true;
    },
    i(local) {
      if (current)
        return;
      transition_in(pause.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(pause.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(pause, detaching);
    }
  };
}
function create_if_block$2(ctx) {
  let div;
  let each_value = ctx[2];
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block$2(get_each_context$2(ctx, each_value, i));
  }
  return {
    c() {
      div = element("div");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      attr(div, "class", "progress-clocks-stopwatch__laps");
    },
    m(target, anchor) {
      insert(target, div, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(div, null);
        }
      }
    },
    p(ctx2, dirty) {
      if (dirty & 517) {
        each_value = ctx2[2];
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context$2(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block$2(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(div, null);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value.length;
      }
    },
    d(detaching) {
      if (detaching)
        detach(div);
      destroy_each(each_blocks, detaching);
    }
  };
}
function create_each_block$2(ctx) {
  let div;
  let t0;
  let t1_value = ctx[20] + 1 + "";
  let t1;
  let t2;
  let t3_value = ctx[9](ctx[18], ctx[0]) + "";
  let t3;
  let div_data_lap_time_ms_value;
  return {
    c() {
      div = element("div");
      t0 = text("(");
      t1 = text(t1_value);
      t2 = text(") ");
      t3 = text(t3_value);
      attr(div, "data-lap-time-ms", div_data_lap_time_ms_value = ctx[18]);
    },
    m(target, anchor) {
      insert(target, div, anchor);
      append(div, t0);
      append(div, t1);
      append(div, t2);
      append(div, t3);
    },
    p(ctx2, dirty) {
      if (dirty & 5 && t3_value !== (t3_value = ctx2[9](ctx2[18], ctx2[0]) + ""))
        set_data(t3, t3_value);
      if (dirty & 4 && div_data_lap_time_ms_value !== (div_data_lap_time_ms_value = ctx2[18])) {
        attr(div, "data-lap-time-ms", div_data_lap_time_ms_value);
      }
    },
    d(detaching) {
      if (detaching)
        detach(div);
    }
  };
}
function create_fragment$2(ctx) {
  let div2;
  let div0;
  let t0_value = ctx[9](ctx[8], ctx[0]) + "";
  let t0;
  let t1;
  let div1;
  let button0;
  let current_block_type_index;
  let if_block0;
  let t2;
  let button1;
  let refreshccw;
  let t3;
  let button2;
  let timer;
  let t4;
  let button3;
  let t6;
  let current;
  let mounted;
  let dispose;
  const if_block_creators = [create_if_block_1$2, create_else_block$1];
  const if_blocks = [];
  function select_block_type(ctx2, dirty) {
    if (ctx2[1])
      return 0;
    return 1;
  }
  current_block_type_index = select_block_type(ctx);
  if_block0 = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
  refreshccw = new RefreshCcw({});
  timer = new Timer$1({});
  let if_block1 = ctx[2].length > 0 && create_if_block$2(ctx);
  return {
    c() {
      div2 = element("div");
      div0 = element("div");
      t0 = text(t0_value);
      t1 = space();
      div1 = element("div");
      button0 = element("button");
      if_block0.c();
      t2 = space();
      button1 = element("button");
      create_component(refreshccw.$$.fragment);
      t3 = space();
      button2 = element("button");
      create_component(timer.$$.fragment);
      t4 = space();
      button3 = element("button");
      button3.textContent = "/1000";
      t6 = space();
      if (if_block1)
        if_block1.c();
      attr(div0, "class", "progress-clocks-stopwatch__elapsed");
      attr(div0, "role", "button");
      attr(div0, "tabindex", "0");
      attr(div1, "class", "progress-clocks-stopwatch__buttons");
      attr(div2, "class", "progress-clocks-stopwatch");
    },
    m(target, anchor) {
      insert(target, div2, anchor);
      append(div2, div0);
      append(div0, t0);
      append(div2, t1);
      append(div2, div1);
      append(div1, button0);
      if_blocks[current_block_type_index].m(button0, null);
      append(div1, t2);
      append(div1, button1);
      mount_component(refreshccw, button1, null);
      append(div1, t3);
      append(div1, button2);
      mount_component(timer, button2, null);
      append(div1, t4);
      append(div1, button3);
      append(div2, t6);
      if (if_block1)
        if_block1.m(div2, null);
      current = true;
      if (!mounted) {
        dispose = [
          listen(div0, "click", ctx[6]),
          listen(div0, "keydown", ifClickEquivalent(ctx[6])),
          listen(button0, "click", ctx[12]),
          listen(button1, "click", ctx[5]),
          listen(button2, "click", ctx[7]),
          listen(button3, "click", ctx[13])
        ];
        mounted = true;
      }
    },
    p(ctx2, [dirty]) {
      if ((!current || dirty & 257) && t0_value !== (t0_value = ctx2[9](ctx2[8], ctx2[0]) + ""))
        set_data(t0, t0_value);
      let previous_block_index = current_block_type_index;
      current_block_type_index = select_block_type(ctx2);
      if (current_block_type_index !== previous_block_index) {
        group_outros();
        transition_out(if_blocks[previous_block_index], 1, 1, () => {
          if_blocks[previous_block_index] = null;
        });
        check_outros();
        if_block0 = if_blocks[current_block_type_index];
        if (!if_block0) {
          if_block0 = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx2);
          if_block0.c();
        }
        transition_in(if_block0, 1);
        if_block0.m(button0, null);
      }
      if (ctx2[2].length > 0) {
        if (if_block1) {
          if_block1.p(ctx2, dirty);
        } else {
          if_block1 = create_if_block$2(ctx2);
          if_block1.c();
          if_block1.m(div2, null);
        }
      } else if (if_block1) {
        if_block1.d(1);
        if_block1 = null;
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(if_block0);
      transition_in(refreshccw.$$.fragment, local);
      transition_in(timer.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(if_block0);
      transition_out(refreshccw.$$.fragment, local);
      transition_out(timer.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      if (detaching)
        detach(div2);
      if_blocks[current_block_type_index].d();
      destroy_component(refreshccw);
      destroy_component(timer);
      if (if_block1)
        if_block1.d();
      mounted = false;
      run_all(dispose);
    }
  };
}
const TICK_INTERVAL_MS = 10;
function instance$2($$self, $$props, $$invalidate) {
  const dispatch2 = createEventDispatcher();
  const locale = Intl.NumberFormat().resolvedOptions().locale;
  let { startMillis = new Date().getTime() } = $$props;
  let { offsetMillis = 0 } = $$props;
  let { showMillis = false } = $$props;
  let { isRunning = true } = $$props;
  let { lapTimes = [] } = $$props;
  let elapsedMs = 0;
  let tickInterval = null;
  function tick2() {
    $$invalidate(8, elapsedMs = new Date().getTime() - startMillis + offsetMillis);
  }
  onMount(() => {
    if (isRunning) {
      tick2();
      start();
    } else {
      $$invalidate(8, elapsedMs = offsetMillis);
    }
  });
  onDestroy(() => {
    if (tickInterval) {
      window.clearInterval(tickInterval);
      tickInterval = null;
    }
  });
  function start() {
    if (tickInterval) {
      window.clearInterval(tickInterval);
      tickInterval = null;
    }
    $$invalidate(11, offsetMillis = elapsedMs);
    $$invalidate(10, startMillis = new Date().getTime());
    tickInterval = window.setInterval(tick2, TICK_INTERVAL_MS);
    $$invalidate(1, isRunning = true);
  }
  function stop() {
    if (tickInterval) {
      window.clearInterval(tickInterval);
      tickInterval = null;
    }
    $$invalidate(11, offsetMillis = elapsedMs);
    $$invalidate(1, isRunning = false);
  }
  function reset() {
    $$invalidate(10, startMillis = new Date().getTime());
    $$invalidate(11, offsetMillis = 0);
    $$invalidate(2, lapTimes = []);
    $$invalidate(8, elapsedMs = 0);
  }
  function togglePrecision() {
    $$invalidate(0, showMillis = !showMillis);
  }
  function lap() {
    lapTimes.push(elapsedMs);
    $$invalidate(2, lapTimes);
    dispatch2("lap", { elapsedMs });
  }
  function formatTime(ms, showMillis2 = false) {
    const seconds = showMillis2 ? ms / 1e3 % 60 : Math.floor(ms / 1e3) % 60;
    const secondsFormatted = Intl.NumberFormat(locale, {
      style: "decimal",
      minimumIntegerDigits: 2,
      minimumFractionDigits: showMillis2 ? 3 : 0
    }).format(seconds);
    const minutes = Math.floor(ms / 1e3 / 60) % 60;
    const minutesFormatted = Intl.NumberFormat(locale, {
      style: "decimal",
      minimumIntegerDigits: 2
    }).format(minutes);
    const hours = Math.floor(ms / 1e3 / 60 / 60);
    const hoursFormatted = Intl.NumberFormat(locale, {
      style: "decimal",
      minimumIntegerDigits: 2
    }).format(hours);
    return hours > 0 ? `${hoursFormatted}:${minutesFormatted}:${secondsFormatted}` : `${minutesFormatted}:${secondsFormatted}`;
  }
  const click_handler = () => isRunning ? stop() : start();
  const click_handler_1 = () => $$invalidate(0, showMillis = !showMillis);
  $$self.$$set = ($$props2) => {
    if ("startMillis" in $$props2)
      $$invalidate(10, startMillis = $$props2.startMillis);
    if ("offsetMillis" in $$props2)
      $$invalidate(11, offsetMillis = $$props2.offsetMillis);
    if ("showMillis" in $$props2)
      $$invalidate(0, showMillis = $$props2.showMillis);
    if ("isRunning" in $$props2)
      $$invalidate(1, isRunning = $$props2.isRunning);
    if ("lapTimes" in $$props2)
      $$invalidate(2, lapTimes = $$props2.lapTimes);
  };
  return [
    showMillis,
    isRunning,
    lapTimes,
    start,
    stop,
    reset,
    togglePrecision,
    lap,
    elapsedMs,
    formatTime,
    startMillis,
    offsetMillis,
    click_handler,
    click_handler_1
  ];
}
class StopWatch extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$2, create_fragment$2, safe_not_equal, {
      startMillis: 10,
      offsetMillis: 11,
      showMillis: 0,
      isRunning: 1,
      lapTimes: 2,
      start: 3,
      stop: 4,
      reset: 5,
      togglePrecision: 6,
      lap: 7
    });
  }
  get start() {
    return this.$$.ctx[3];
  }
  get stop() {
    return this.$$.ctx[4];
  }
  get reset() {
    return this.$$.ctx[5];
  }
  get togglePrecision() {
    return this.$$.ctx[6];
  }
  get lap() {
    return this.$$.ctx[7];
  }
}
function get_each_context$1(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[27] = list[i];
  child_ctx[28] = list;
  child_ctx[29] = i;
  return child_ctx;
}
function create_if_block_3(ctx) {
  let stopwatch;
  let updating_startMillis;
  let updating_offsetMillis;
  let updating_showMillis;
  let updating_isRunning;
  let updating_lapTimes;
  let current;
  const stopwatch_spread_levels = [ctx[27]];
  function stopwatch_startMillis_binding(value) {
    ctx[14](value, ctx[27]);
  }
  function stopwatch_offsetMillis_binding(value) {
    ctx[15](value, ctx[27]);
  }
  function stopwatch_showMillis_binding(value) {
    ctx[16](value, ctx[27]);
  }
  function stopwatch_isRunning_binding(value) {
    ctx[17](value, ctx[27]);
  }
  function stopwatch_lapTimes_binding(value) {
    ctx[18](value, ctx[27]);
  }
  let stopwatch_props = {};
  for (let i = 0; i < stopwatch_spread_levels.length; i += 1) {
    stopwatch_props = assign(stopwatch_props, stopwatch_spread_levels[i]);
  }
  if (ctx[27].startMillis !== void 0) {
    stopwatch_props.startMillis = ctx[27].startMillis;
  }
  if (ctx[27].offsetMillis !== void 0) {
    stopwatch_props.offsetMillis = ctx[27].offsetMillis;
  }
  if (ctx[27].showMillis !== void 0) {
    stopwatch_props.showMillis = ctx[27].showMillis;
  }
  if (ctx[27].isRunning !== void 0) {
    stopwatch_props.isRunning = ctx[27].isRunning;
  }
  if (ctx[27].lapTimes !== void 0) {
    stopwatch_props.lapTimes = ctx[27].lapTimes;
  }
  stopwatch = new StopWatch({ props: stopwatch_props });
  binding_callbacks.push(() => bind(stopwatch, "startMillis", stopwatch_startMillis_binding));
  binding_callbacks.push(() => bind(stopwatch, "offsetMillis", stopwatch_offsetMillis_binding));
  binding_callbacks.push(() => bind(stopwatch, "showMillis", stopwatch_showMillis_binding));
  binding_callbacks.push(() => bind(stopwatch, "isRunning", stopwatch_isRunning_binding));
  binding_callbacks.push(() => bind(stopwatch, "lapTimes", stopwatch_lapTimes_binding));
  return {
    c() {
      create_component(stopwatch.$$.fragment);
    },
    m(target, anchor) {
      mount_component(stopwatch, target, anchor);
      current = true;
    },
    p(new_ctx, dirty) {
      ctx = new_ctx;
      const stopwatch_changes = dirty & 2 ? get_spread_update(stopwatch_spread_levels, [get_spread_object(ctx[27])]) : {};
      if (!updating_startMillis && dirty & 2) {
        updating_startMillis = true;
        stopwatch_changes.startMillis = ctx[27].startMillis;
        add_flush_callback(() => updating_startMillis = false);
      }
      if (!updating_offsetMillis && dirty & 2) {
        updating_offsetMillis = true;
        stopwatch_changes.offsetMillis = ctx[27].offsetMillis;
        add_flush_callback(() => updating_offsetMillis = false);
      }
      if (!updating_showMillis && dirty & 2) {
        updating_showMillis = true;
        stopwatch_changes.showMillis = ctx[27].showMillis;
        add_flush_callback(() => updating_showMillis = false);
      }
      if (!updating_isRunning && dirty & 2) {
        updating_isRunning = true;
        stopwatch_changes.isRunning = ctx[27].isRunning;
        add_flush_callback(() => updating_isRunning = false);
      }
      if (!updating_lapTimes && dirty & 2) {
        updating_lapTimes = true;
        stopwatch_changes.lapTimes = ctx[27].lapTimes;
        add_flush_callback(() => updating_lapTimes = false);
      }
      stopwatch.$set(stopwatch_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(stopwatch.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(stopwatch.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(stopwatch, detaching);
    }
  };
}
function create_if_block_2$1(ctx) {
  let counter;
  let updating_value;
  let current;
  const counter_spread_levels = [ctx[27]];
  function counter_value_binding(value) {
    ctx[13](value, ctx[27]);
  }
  let counter_props = {};
  for (let i = 0; i < counter_spread_levels.length; i += 1) {
    counter_props = assign(counter_props, counter_spread_levels[i]);
  }
  if (ctx[27].value !== void 0) {
    counter_props.value = ctx[27].value;
  }
  counter = new Counter({ props: counter_props });
  binding_callbacks.push(() => bind(counter, "value", counter_value_binding));
  return {
    c() {
      create_component(counter.$$.fragment);
    },
    m(target, anchor) {
      mount_component(counter, target, anchor);
      current = true;
    },
    p(new_ctx, dirty) {
      ctx = new_ctx;
      const counter_changes = dirty & 2 ? get_spread_update(counter_spread_levels, [get_spread_object(ctx[27])]) : {};
      if (!updating_value && dirty & 2) {
        updating_value = true;
        counter_changes.value = ctx[27].value;
        add_flush_callback(() => updating_value = false);
      }
      counter.$set(counter_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(counter.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(counter.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(counter, detaching);
    }
  };
}
function create_if_block_1$1(ctx) {
  let clock;
  let updating_segments;
  let updating_filled;
  let current;
  const clock_spread_levels = [ctx[27]];
  function clock_segments_binding(value) {
    ctx[11](value, ctx[27]);
  }
  function clock_filled_binding(value) {
    ctx[12](value, ctx[27]);
  }
  let clock_props = {};
  for (let i = 0; i < clock_spread_levels.length; i += 1) {
    clock_props = assign(clock_props, clock_spread_levels[i]);
  }
  if (ctx[27].segments !== void 0) {
    clock_props.segments = ctx[27].segments;
  }
  if (ctx[27].filled !== void 0) {
    clock_props.filled = ctx[27].filled;
  }
  clock = new Clock({ props: clock_props });
  binding_callbacks.push(() => bind(clock, "segments", clock_segments_binding));
  binding_callbacks.push(() => bind(clock, "filled", clock_filled_binding));
  return {
    c() {
      create_component(clock.$$.fragment);
    },
    m(target, anchor) {
      mount_component(clock, target, anchor);
      current = true;
    },
    p(new_ctx, dirty) {
      ctx = new_ctx;
      const clock_changes = dirty & 2 ? get_spread_update(clock_spread_levels, [get_spread_object(ctx[27])]) : {};
      if (!updating_segments && dirty & 2) {
        updating_segments = true;
        clock_changes.segments = ctx[27].segments;
        add_flush_callback(() => updating_segments = false);
      }
      if (!updating_filled && dirty & 2) {
        updating_filled = true;
        clock_changes.filled = ctx[27].filled;
        add_flush_callback(() => updating_filled = false);
      }
      clock.$set(clock_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(clock.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(clock.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(clock, detaching);
    }
  };
}
function create_each_block$1(ctx) {
  let div3;
  let current_block_type_index;
  let if_block;
  let t0;
  let div0;
  let editabletext;
  let updating_value;
  let t1;
  let div2;
  let div1;
  let trash2;
  let t2;
  let div3_data_child_type_value;
  let current;
  let mounted;
  let dispose;
  const if_block_creators = [create_if_block_1$1, create_if_block_2$1, create_if_block_3];
  const if_blocks = [];
  function select_block_type(ctx2, dirty) {
    if (ctx2[27].type === "clock")
      return 0;
    if (ctx2[27].type === "counter")
      return 1;
    if (ctx2[27].type === "stopwatch")
      return 2;
    return -1;
  }
  if (~(current_block_type_index = select_block_type(ctx))) {
    if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
  }
  function editabletext_value_binding_1(value) {
    ctx[19](value, ctx[27]);
  }
  let editabletext_props = {};
  if (ctx[27].name !== void 0) {
    editabletext_props.value = ctx[27].name;
  }
  editabletext = new EditableText({ props: editabletext_props });
  binding_callbacks.push(() => bind(editabletext, "value", editabletext_value_binding_1));
  trash2 = new Trash2({});
  function click_handler() {
    return ctx[20](ctx[29]);
  }
  function keydown_handler() {
    return ctx[21](ctx[29]);
  }
  return {
    c() {
      div3 = element("div");
      if (if_block)
        if_block.c();
      t0 = space();
      div0 = element("div");
      create_component(editabletext.$$.fragment);
      t1 = space();
      div2 = element("div");
      div1 = element("div");
      create_component(trash2.$$.fragment);
      t2 = space();
      attr(div0, "class", "progress-clocks-section__child-name");
      attr(div1, "role", "button");
      attr(div1, "tabindex", "0");
      attr(div1, "class", "progress-clocks-button progress-clocks-section__remove-child");
      attr(div2, "class", "progress-clocks-section__remove-child");
      attr(div3, "class", "progress-clocks-section__child");
      attr(div3, "data-child-type", div3_data_child_type_value = ctx[27].type);
    },
    m(target, anchor) {
      insert(target, div3, anchor);
      if (~current_block_type_index) {
        if_blocks[current_block_type_index].m(div3, null);
      }
      append(div3, t0);
      append(div3, div0);
      mount_component(editabletext, div0, null);
      append(div3, t1);
      append(div3, div2);
      append(div2, div1);
      mount_component(trash2, div1, null);
      append(div3, t2);
      current = true;
      if (!mounted) {
        dispose = [
          listen(div1, "click", click_handler),
          listen(div1, "keydown", ifClickEquivalent(keydown_handler))
        ];
        mounted = true;
      }
    },
    p(new_ctx, dirty) {
      ctx = new_ctx;
      let previous_block_index = current_block_type_index;
      current_block_type_index = select_block_type(ctx);
      if (current_block_type_index === previous_block_index) {
        if (~current_block_type_index) {
          if_blocks[current_block_type_index].p(ctx, dirty);
        }
      } else {
        if (if_block) {
          group_outros();
          transition_out(if_blocks[previous_block_index], 1, 1, () => {
            if_blocks[previous_block_index] = null;
          });
          check_outros();
        }
        if (~current_block_type_index) {
          if_block = if_blocks[current_block_type_index];
          if (!if_block) {
            if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
            if_block.c();
          } else {
            if_block.p(ctx, dirty);
          }
          transition_in(if_block, 1);
          if_block.m(div3, t0);
        } else {
          if_block = null;
        }
      }
      const editabletext_changes = {};
      if (!updating_value && dirty & 2) {
        updating_value = true;
        editabletext_changes.value = ctx[27].name;
        add_flush_callback(() => updating_value = false);
      }
      editabletext.$set(editabletext_changes);
      if (!current || dirty & 2 && div3_data_child_type_value !== (div3_data_child_type_value = ctx[27].type)) {
        attr(div3, "data-child-type", div3_data_child_type_value);
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(if_block);
      transition_in(editabletext.$$.fragment, local);
      transition_in(trash2.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(if_block);
      transition_out(editabletext.$$.fragment, local);
      transition_out(trash2.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      if (detaching)
        detach(div3);
      if (~current_block_type_index) {
        if_blocks[current_block_type_index].d();
      }
      destroy_component(editabletext);
      destroy_component(trash2);
      mounted = false;
      run_all(dispose);
    }
  };
}
function create_else_block(ctx) {
  let button;
  let piechart;
  let current;
  let mounted;
  let dispose;
  piechart = new PieChart({});
  return {
    c() {
      button = element("button");
      create_component(piechart.$$.fragment);
      attr(button, "class", "progress-clocks-section__add-clock");
      attr(button, "title", "Add new progress clock");
    },
    m(target, anchor) {
      insert(target, button, anchor);
      mount_component(piechart, button, null);
      current = true;
      if (!mounted) {
        dispose = listen(button, "click", ctx[25]);
        mounted = true;
      }
    },
    p: noop,
    i(local) {
      if (current)
        return;
      transition_in(piechart.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(piechart.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      if (detaching)
        detach(button);
      destroy_component(piechart);
      mounted = false;
      dispose();
    }
  };
}
function create_if_block$1(ctx) {
  let editablenumber;
  let updating_mode;
  let updating_value;
  let current;
  function editablenumber_mode_binding(value) {
    ctx[22](value);
  }
  function editablenumber_value_binding(value) {
    ctx[23](value);
  }
  let editablenumber_props = {};
  if (ctx[3] !== void 0) {
    editablenumber_props.mode = ctx[3];
  }
  if (ctx[4] !== void 0) {
    editablenumber_props.value = ctx[4];
  }
  editablenumber = new EditableNumber({ props: editablenumber_props });
  binding_callbacks.push(() => bind(editablenumber, "mode", editablenumber_mode_binding));
  binding_callbacks.push(() => bind(editablenumber, "value", editablenumber_value_binding));
  editablenumber.$on("confirmed", ctx[6]);
  editablenumber.$on("cancelled", ctx[24]);
  return {
    c() {
      create_component(editablenumber.$$.fragment);
    },
    m(target, anchor) {
      mount_component(editablenumber, target, anchor);
      current = true;
    },
    p(ctx2, dirty) {
      const editablenumber_changes = {};
      if (!updating_mode && dirty & 8) {
        updating_mode = true;
        editablenumber_changes.mode = ctx2[3];
        add_flush_callback(() => updating_mode = false);
      }
      if (!updating_value && dirty & 16) {
        updating_value = true;
        editablenumber_changes.value = ctx2[4];
        add_flush_callback(() => updating_value = false);
      }
      editablenumber.$set(editablenumber_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(editablenumber.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(editablenumber.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(editablenumber, detaching);
    }
  };
}
function create_fragment$1(ctx) {
  let section;
  let div0;
  let editabletext;
  let updating_value;
  let t0;
  let div1;
  let trash2;
  let t1;
  let div2;
  let t2;
  let div3;
  let current_block_type_index;
  let if_block;
  let t3;
  let button0;
  let plussquare;
  let t4;
  let button1;
  let timer;
  let section_transition;
  let current;
  let mounted;
  let dispose;
  function editabletext_value_binding(value) {
    ctx[10](value);
  }
  let editabletext_props = {};
  if (ctx[0] !== void 0) {
    editabletext_props.value = ctx[0];
  }
  editabletext = new EditableText({ props: editabletext_props });
  binding_callbacks.push(() => bind(editabletext, "value", editabletext_value_binding));
  trash2 = new Trash2({});
  let each_value = ctx[1];
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block$1(get_each_context$1(ctx, each_value, i));
  }
  const out = (i) => transition_out(each_blocks[i], 1, 1, () => {
    each_blocks[i] = null;
  });
  const if_block_creators = [create_if_block$1, create_else_block];
  const if_blocks = [];
  function select_block_type_1(ctx2, dirty) {
    if (ctx2[2])
      return 0;
    return 1;
  }
  current_block_type_index = select_block_type_1(ctx);
  if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
  plussquare = new PlusSquare({});
  timer = new Timer$1({});
  return {
    c() {
      section = element("section");
      div0 = element("div");
      create_component(editabletext.$$.fragment);
      t0 = space();
      div1 = element("div");
      create_component(trash2.$$.fragment);
      t1 = space();
      div2 = element("div");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      t2 = space();
      div3 = element("div");
      if_block.c();
      t3 = space();
      button0 = element("button");
      create_component(plussquare.$$.fragment);
      t4 = space();
      button1 = element("button");
      create_component(timer.$$.fragment);
      attr(div0, "class", "progress-clocks-section__name");
      attr(div1, "role", "button");
      attr(div1, "tabindex", "0");
      attr(div1, "class", "progress-clocks-button progress-clocks-section__remove");
      attr(div2, "class", "progress-clocks-section__children");
      attr(button0, "class", "progress-clocks-section__add-counter");
      attr(button0, "title", "Add new counter");
      attr(button1, "class", "progress-clocks-section__add-stopwatch");
      attr(button1, "title", "Add new stopwatch");
      attr(div3, "class", "progress-clocks-section__add-child");
      attr(section, "class", "progress-clocks-section");
    },
    m(target, anchor) {
      insert(target, section, anchor);
      append(section, div0);
      mount_component(editabletext, div0, null);
      append(section, t0);
      append(section, div1);
      mount_component(trash2, div1, null);
      append(section, t1);
      append(section, div2);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(div2, null);
        }
      }
      append(section, t2);
      append(section, div3);
      if_blocks[current_block_type_index].m(div3, null);
      append(div3, t3);
      append(div3, button0);
      mount_component(plussquare, button0, null);
      append(div3, t4);
      append(div3, button1);
      mount_component(timer, button1, null);
      current = true;
      if (!mounted) {
        dispose = [
          listen(div1, "click", ctx[5]),
          listen(div1, "contextmenu", ctx[5]),
          listen(div1, "keydown", ctx[5]),
          listen(button0, "click", ctx[7]),
          listen(button1, "click", ctx[8])
        ];
        mounted = true;
      }
    },
    p(ctx2, [dirty]) {
      const editabletext_changes = {};
      if (!updating_value && dirty & 1) {
        updating_value = true;
        editabletext_changes.value = ctx2[0];
        add_flush_callback(() => updating_value = false);
      }
      editabletext.$set(editabletext_changes);
      if (dirty & 514) {
        each_value = ctx2[1];
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context$1(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
            transition_in(each_blocks[i], 1);
          } else {
            each_blocks[i] = create_each_block$1(child_ctx);
            each_blocks[i].c();
            transition_in(each_blocks[i], 1);
            each_blocks[i].m(div2, null);
          }
        }
        group_outros();
        for (i = each_value.length; i < each_blocks.length; i += 1) {
          out(i);
        }
        check_outros();
      }
      let previous_block_index = current_block_type_index;
      current_block_type_index = select_block_type_1(ctx2);
      if (current_block_type_index === previous_block_index) {
        if_blocks[current_block_type_index].p(ctx2, dirty);
      } else {
        group_outros();
        transition_out(if_blocks[previous_block_index], 1, 1, () => {
          if_blocks[previous_block_index] = null;
        });
        check_outros();
        if_block = if_blocks[current_block_type_index];
        if (!if_block) {
          if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx2);
          if_block.c();
        } else {
          if_block.p(ctx2, dirty);
        }
        transition_in(if_block, 1);
        if_block.m(div3, t3);
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(editabletext.$$.fragment, local);
      transition_in(trash2.$$.fragment, local);
      for (let i = 0; i < each_value.length; i += 1) {
        transition_in(each_blocks[i]);
      }
      transition_in(if_block);
      transition_in(plussquare.$$.fragment, local);
      transition_in(timer.$$.fragment, local);
      add_render_callback(() => {
        if (!current)
          return;
        if (!section_transition)
          section_transition = create_bidirectional_transition(section, fade, { duration: 100 }, true);
        section_transition.run(1);
      });
      current = true;
    },
    o(local) {
      transition_out(editabletext.$$.fragment, local);
      transition_out(trash2.$$.fragment, local);
      each_blocks = each_blocks.filter(Boolean);
      for (let i = 0; i < each_blocks.length; i += 1) {
        transition_out(each_blocks[i]);
      }
      transition_out(if_block);
      transition_out(plussquare.$$.fragment, local);
      transition_out(timer.$$.fragment, local);
      if (!section_transition)
        section_transition = create_bidirectional_transition(section, fade, { duration: 100 }, false);
      section_transition.run(0);
      current = false;
    },
    d(detaching) {
      if (detaching)
        detach(section);
      destroy_component(editabletext);
      destroy_component(trash2);
      destroy_each(each_blocks, detaching);
      if_blocks[current_block_type_index].d();
      destroy_component(plussquare);
      destroy_component(timer);
      if (detaching && section_transition)
        section_transition.end();
      mounted = false;
      run_all(dispose);
    }
  };
}
function instance$1($$self, $$props, $$invalidate) {
  let { name } = $$props;
  let { children: children2 } = $$props;
  const dispatch2 = createEventDispatcher();
  function raiseRemoveSection(e) {
    if (e instanceof MouseEvent || ["Enter", " "].contains(e.key)) {
      dispatch2("removeSection", { self: this });
    }
  }
  let addingClock = false;
  let newClockMode = EditMode.Edit;
  let newClockSegments = 4;
  function addClock() {
    if (newClockMode !== EditMode.Read) {
      return;
    }
    if (newClockSegments < 1) {
      tick().then(() => {
        $$invalidate(3, newClockMode = EditMode.Edit);
      });
      return;
    }
    children2.push({
      type: "clock",
      name: `Clock ${children2.length + 1}`,
      segments: newClockSegments,
      filled: 0
    });
    $$invalidate(2, addingClock = false);
    $$invalidate(3, newClockMode = EditMode.Edit);
    $$invalidate(1, children2);
  }
  function addCounter() {
    children2.push({
      type: "counter",
      name: `Counter ${children2.length + 1}`,
      value: 0
    });
    $$invalidate(1, children2);
  }
  function addStopwatch() {
    children2.push({
      type: "stopwatch",
      name: `Stopwatch ${children2.length + 1}`,
      startMillis: new Date().getTime(),
      offsetMillis: 0,
      showMillis: false,
      isRunning: true,
      lapTimes: []
    });
    $$invalidate(1, children2);
  }
  function removeChild(i) {
    children2.splice(i, 1);
    $$invalidate(1, children2);
  }
  function editabletext_value_binding(value) {
    name = value;
    $$invalidate(0, name);
  }
  function clock_segments_binding(value, child) {
    if ($$self.$$.not_equal(child.segments, value)) {
      child.segments = value;
      $$invalidate(1, children2);
    }
  }
  function clock_filled_binding(value, child) {
    if ($$self.$$.not_equal(child.filled, value)) {
      child.filled = value;
      $$invalidate(1, children2);
    }
  }
  function counter_value_binding(value, child) {
    if ($$self.$$.not_equal(child.value, value)) {
      child.value = value;
      $$invalidate(1, children2);
    }
  }
  function stopwatch_startMillis_binding(value, child) {
    if ($$self.$$.not_equal(child.startMillis, value)) {
      child.startMillis = value;
      $$invalidate(1, children2);
    }
  }
  function stopwatch_offsetMillis_binding(value, child) {
    if ($$self.$$.not_equal(child.offsetMillis, value)) {
      child.offsetMillis = value;
      $$invalidate(1, children2);
    }
  }
  function stopwatch_showMillis_binding(value, child) {
    if ($$self.$$.not_equal(child.showMillis, value)) {
      child.showMillis = value;
      $$invalidate(1, children2);
    }
  }
  function stopwatch_isRunning_binding(value, child) {
    if ($$self.$$.not_equal(child.isRunning, value)) {
      child.isRunning = value;
      $$invalidate(1, children2);
    }
  }
  function stopwatch_lapTimes_binding(value, child) {
    if ($$self.$$.not_equal(child.lapTimes, value)) {
      child.lapTimes = value;
      $$invalidate(1, children2);
    }
  }
  function editabletext_value_binding_1(value, child) {
    if ($$self.$$.not_equal(child.name, value)) {
      child.name = value;
      $$invalidate(1, children2);
    }
  }
  const click_handler = (i) => removeChild(i);
  const keydown_handler = (i) => removeChild(i);
  function editablenumber_mode_binding(value) {
    newClockMode = value;
    $$invalidate(3, newClockMode);
  }
  function editablenumber_value_binding(value) {
    newClockSegments = value;
    $$invalidate(4, newClockSegments);
  }
  const cancelled_handler = () => {
    $$invalidate(2, addingClock = false);
    $$invalidate(3, newClockMode = EditMode.Edit);
  };
  const click_handler_1 = () => $$invalidate(2, addingClock = true);
  $$self.$$set = ($$props2) => {
    if ("name" in $$props2)
      $$invalidate(0, name = $$props2.name);
    if ("children" in $$props2)
      $$invalidate(1, children2 = $$props2.children);
  };
  return [
    name,
    children2,
    addingClock,
    newClockMode,
    newClockSegments,
    raiseRemoveSection,
    addClock,
    addCounter,
    addStopwatch,
    removeChild,
    editabletext_value_binding,
    clock_segments_binding,
    clock_filled_binding,
    counter_value_binding,
    stopwatch_startMillis_binding,
    stopwatch_offsetMillis_binding,
    stopwatch_showMillis_binding,
    stopwatch_isRunning_binding,
    stopwatch_lapTimes_binding,
    editabletext_value_binding_1,
    click_handler,
    keydown_handler,
    editablenumber_mode_binding,
    editablenumber_value_binding,
    cancelled_handler,
    click_handler_1
  ];
}
class Section extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$1, create_fragment$1, safe_not_equal, { name: 0, children: 1 });
  }
}
function get_each_context(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[9] = list[i];
  child_ctx[10] = list;
  child_ctx[11] = i;
  return child_ctx;
}
function create_if_block_2(ctx) {
  let header;
  return {
    c() {
      header = element("header");
      header.innerHTML = `<span class="progress-clocks-title__main-title">Progress Clocks</span> 
      <a class="progress-clocks-title__subtitle" href="https://github.com/tokenshift/obsidian-progress-clocks">https://github.com/tokenshift/obsidian-progress-clocks</a>`;
      attr(header, "class", "progress-clocks-title");
    },
    m(target, anchor) {
      insert(target, header, anchor);
    },
    d(detaching) {
      if (detaching)
        detach(header);
    }
  };
}
function create_each_block(ctx) {
  let section;
  let updating_name;
  let updating_children;
  let current;
  function section_name_binding(value) {
    ctx[5](value, ctx[9]);
  }
  function section_children_binding(value) {
    ctx[6](value, ctx[9]);
  }
  function removeSection_handler() {
    return ctx[7](ctx[11]);
  }
  let section_props = {};
  if (ctx[9].name !== void 0) {
    section_props.name = ctx[9].name;
  }
  if (ctx[9].children !== void 0) {
    section_props.children = ctx[9].children;
  }
  section = new Section({ props: section_props });
  binding_callbacks.push(() => bind(section, "name", section_name_binding));
  binding_callbacks.push(() => bind(section, "children", section_children_binding));
  section.$on("removeSection", removeSection_handler);
  return {
    c() {
      create_component(section.$$.fragment);
    },
    m(target, anchor) {
      mount_component(section, target, anchor);
      current = true;
    },
    p(new_ctx, dirty) {
      ctx = new_ctx;
      const section_changes = {};
      if (!updating_name && dirty & 1) {
        updating_name = true;
        section_changes.name = ctx[9].name;
        add_flush_callback(() => updating_name = false);
      }
      if (!updating_children && dirty & 1) {
        updating_children = true;
        section_changes.children = ctx[9].children;
        add_flush_callback(() => updating_children = false);
      }
      section.$set(section_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(section.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(section.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(section, detaching);
    }
  };
}
function create_if_block_1(ctx) {
  let pre;
  let t0;
  let t1_value = JSON.stringify(ctx[0], null, 2) + "";
  let t1;
  let t2;
  return {
    c() {
      pre = element("pre");
      t0 = text("  ");
      t1 = text(t1_value);
      t2 = text("\n  ");
      attr(pre, "class", "progress-clocks-debug");
    },
    m(target, anchor) {
      insert(target, pre, anchor);
      append(pre, t0);
      append(pre, t1);
      append(pre, t2);
    },
    p(ctx2, dirty) {
      if (dirty & 1 && t1_value !== (t1_value = JSON.stringify(ctx2[0], null, 2) + ""))
        set_data(t1, t1_value);
    },
    d(detaching) {
      if (detaching)
        detach(pre);
    }
  };
}
function create_if_block(ctx) {
  let div;
  let t0;
  let t1;
  return {
    c() {
      div = element("div");
      t0 = text("Counters v");
      t1 = text(ctx[1]);
      attr(div, "class", "progress-clocks-panel__version");
    },
    m(target, anchor) {
      insert(target, div, anchor);
      append(div, t0);
      append(div, t1);
    },
    p(ctx2, dirty) {
      if (dirty & 2)
        set_data(t1, ctx2[1]);
    },
    d(detaching) {
      if (detaching)
        detach(div);
    }
  };
}
function create_fragment(ctx) {
  let div1;
  let t0;
  let t1;
  let div0;
  let t3;
  let t4;
  let current;
  let mounted;
  let dispose;
  let if_block0 = ctx[2] && create_if_block_2();
  let each_value = ctx[0].sections;
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block(get_each_context(ctx, each_value, i));
  }
  const out = (i) => transition_out(each_blocks[i], 1, 1, () => {
    each_blocks[i] = null;
  });
  let if_block1 = ctx[0].debug && create_if_block_1(ctx);
  let if_block2 = ctx[1] && create_if_block(ctx);
  return {
    c() {
      div1 = element("div");
      if (if_block0)
        if_block0.c();
      t0 = space();
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      t1 = space();
      div0 = element("div");
      div0.textContent = "Add Section";
      t3 = space();
      if (if_block1)
        if_block1.c();
      t4 = space();
      if (if_block2)
        if_block2.c();
      attr(div0, "class", "progress-clocks-button progress-clocks-panel__add-section");
      attr(div0, "role", "button");
      attr(div0, "tabindex", "0");
      attr(div1, "class", "progress-clocks progress-clocks-panel");
    },
    m(target, anchor) {
      insert(target, div1, anchor);
      if (if_block0)
        if_block0.m(div1, null);
      append(div1, t0);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(div1, null);
        }
      }
      append(div1, t1);
      append(div1, div0);
      append(div1, t3);
      if (if_block1)
        if_block1.m(div1, null);
      append(div1, t4);
      if (if_block2)
        if_block2.m(div1, null);
      current = true;
      if (!mounted) {
        dispose = [
          listen(div0, "keydown", ifClickEquivalent(ctx[3])),
          listen(div0, "click", ctx[3])
        ];
        mounted = true;
      }
    },
    p(ctx2, [dirty]) {
      if (ctx2[2]) {
        if (if_block0)
          ;
        else {
          if_block0 = create_if_block_2();
          if_block0.c();
          if_block0.m(div1, t0);
        }
      } else if (if_block0) {
        if_block0.d(1);
        if_block0 = null;
      }
      if (dirty & 17) {
        each_value = ctx2[0].sections;
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
            transition_in(each_blocks[i], 1);
          } else {
            each_blocks[i] = create_each_block(child_ctx);
            each_blocks[i].c();
            transition_in(each_blocks[i], 1);
            each_blocks[i].m(div1, t1);
          }
        }
        group_outros();
        for (i = each_value.length; i < each_blocks.length; i += 1) {
          out(i);
        }
        check_outros();
      }
      if (ctx2[0].debug) {
        if (if_block1) {
          if_block1.p(ctx2, dirty);
        } else {
          if_block1 = create_if_block_1(ctx2);
          if_block1.c();
          if_block1.m(div1, t4);
        }
      } else if (if_block1) {
        if_block1.d(1);
        if_block1 = null;
      }
      if (ctx2[1]) {
        if (if_block2) {
          if_block2.p(ctx2, dirty);
        } else {
          if_block2 = create_if_block(ctx2);
          if_block2.c();
          if_block2.m(div1, null);
        }
      } else if (if_block2) {
        if_block2.d(1);
        if_block2 = null;
      }
    },
    i(local) {
      if (current)
        return;
      for (let i = 0; i < each_value.length; i += 1) {
        transition_in(each_blocks[i]);
      }
      current = true;
    },
    o(local) {
      each_blocks = each_blocks.filter(Boolean);
      for (let i = 0; i < each_blocks.length; i += 1) {
        transition_out(each_blocks[i]);
      }
      current = false;
    },
    d(detaching) {
      if (detaching)
        detach(div1);
      if (if_block0)
        if_block0.d();
      destroy_each(each_blocks, detaching);
      if (if_block1)
        if_block1.d();
      if (if_block2)
        if_block2.d();
      mounted = false;
      run_all(dispose);
    }
  };
}
function instance($$self, $$props, $$invalidate) {
  const dispatch2 = createEventDispatcher();
  let { state = new State() } = $$props;
  let { version } = $$props;
  let { showTitle = false } = $$props;
  function addSection() {
    state.sections.push({
      name: `Section ${state.sections.length + 1}`,
      children: []
    });
    $$invalidate(0, state);
  }
  function removeSection(i) {
    state.sections.splice(i, 1);
    $$invalidate(0, state);
  }
  function section_name_binding(value, section) {
    if ($$self.$$.not_equal(section.name, value)) {
      section.name = value;
      $$invalidate(0, state);
    }
  }
  function section_children_binding(value, section) {
    if ($$self.$$.not_equal(section.children, value)) {
      section.children = value;
      $$invalidate(0, state);
    }
  }
  const removeSection_handler = (i) => removeSection(i);
  $$self.$$set = ($$props2) => {
    if ("state" in $$props2)
      $$invalidate(0, state = $$props2.state);
    if ("version" in $$props2)
      $$invalidate(1, version = $$props2.version);
    if ("showTitle" in $$props2)
      $$invalidate(2, showTitle = $$props2.showTitle);
  };
  $$self.$$.update = () => {
    if ($$self.$$.dirty & 1) {
      dispatch2("stateUpdated", { state });
    }
  };
  return [
    state,
    version,
    showTitle,
    addSection,
    removeSection,
    section_name_binding,
    section_children_binding,
    removeSection_handler
  ];
}
class Panel extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance, create_fragment, safe_not_equal, { state: 0, version: 1, showTitle: 2 });
  }
}
const DISPLAY_TEXT = "Progress Clocks";
const ICON = "pie-chart";
const VIEW_TYPE = "PROGRESS_CLOCKS_VIEW";
const DEBOUNCE_SAVE_STATE_TIME = 1e3;
class ProgressClocksView extends obsidian.ItemView {
  constructor(plugin, leaf) {
    super(leaf);
    __publicField(this, "navigation", false);
    this.plugin = plugin;
    this.leaf = leaf;
  }
  getDisplayText() {
    return DISPLAY_TEXT;
  }
  getIcon() {
    return ICON;
  }
  getViewType() {
    return VIEW_TYPE;
  }
  async onOpen() {
    this.contentEl.empty();
    const data = await this.plugin.loadData();
    const state = (data == null ? void 0 : data.state) || { sections: [] };
    const panel = new Panel({
      target: this.contentEl,
      props: {
        showTitle: true,
        state,
        version: this.plugin.manifest.version
      }
    });
    panel.$on("stateUpdated", obsidian.debounce(({ detail: { state: state2 } }) => {
      this.plugin.saveData({ state: state2 });
    }, DEBOUNCE_SAVE_STATE_TIME, true));
  }
}
class ClockWidget extends view.WidgetType {
  constructor(segments = 4, filled = 0, nodeFrom, nodeTo, showButtonsForInlineClocks, allowClickInteractionForInlineClocks) {
    super();
    this.segments = segments;
    this.filled = filled;
    this.nodeFrom = nodeFrom;
    this.nodeTo = nodeTo;
    this.showButtonsForInlineClocks = showButtonsForInlineClocks;
    this.allowClickInteractionForInlineClocks = allowClickInteractionForInlineClocks;
  }
  toDOM(view2) {
    const container = document.createElement("div");
    container.addClass("progress-clocks-inline");
    const clock = new Clock({
      target: container,
      props: {
        segments: this.segments,
        filled: this.filled,
        showButtonsForInlineClocks: this.showButtonsForInlineClocks,
        allowClickInteractionForInlineClocks: this.allowClickInteractionForInlineClocks
      }
    });
    clock.$on("updated", (event) => {
      const {
        detail: {
          segments,
          filled
        }
      } = event;
      view2.dispatch({
        changes: {
          from: this.nodeFrom,
          to: this.nodeTo,
          insert: `clock ${filled} / ${segments}`
        }
      });
    });
    return container;
  }
}
class CounterWidget extends view.WidgetType {
  constructor(value = 0, nodeFrom, nodeTo) {
    super();
    this.value = value;
    this.nodeFrom = nodeFrom;
    this.nodeTo = nodeTo;
  }
  toDOM(view2) {
    const container = document.createElement("div");
    container.addClass("progress-clocks-inline");
    const counter = new Counter({
      target: container,
      props: {
        value: this.value
      }
    });
    counter.$on("updated", (event) => {
      const {
        detail: {
          value
        }
      } = event;
      view2.dispatch({
        changes: {
          from: this.nodeFrom,
          to: this.nodeTo,
          insert: `counter ${value}`
        }
      });
    });
    return container;
  }
}
const DEFAULT_CLOCK_SEGMENTS = 4;
const CLOCK_PATTERN = new RegExp(/^clock(?:\s+(\d+)\s*(?:\/\s*(\d+))?)?/i);
const COUNTER_PATTERN = new RegExp(/^counter(?:\s+(\d+))?/i);
function isSelectionWithin(selection, rangeFrom, rangeTo) {
  for (const range of selection.ranges) {
    if (range.from <= rangeTo && range.to >= rangeFrom) {
      return true;
    }
  }
  return false;
}
function parseCode(input) {
  input = input.trim();
  let match = CLOCK_PATTERN.exec(input);
  if (match) {
    const segments = match[2] ? Number(match[2]) : match[1] ? Number(match[1]) : DEFAULT_CLOCK_SEGMENTS;
    const filled = match[2] ? Number(match[1]) : 0;
    return {
      type: "clock",
      segments,
      filled
    };
  }
  match = COUNTER_PATTERN.exec(input);
  if (match) {
    const value = match[1] ? Number(match[1]) : 0;
    return {
      type: "counter",
      value
    };
  }
  return null;
}
class InlinePlugin {
  constructor(view$1) {
    __publicField(this, "decorations");
    __publicField(this, "showButtonsForInlineClocks");
    __publicField(this, "allowClickInteractionForInlineClocks");
    this.decorations = view.Decoration.none;
  }
  update(update2) {
    if (update2.docChanged || update2.viewportChanged || update2.selectionSet) {
      if (update2.state.field(obsidian.editorLivePreviewField)) {
        this.decorations = this.inlineRender(update2.view);
      } else {
        this.decorations = view.Decoration.none;
      }
    }
  }
  inlineRender(view$1) {
    const widgets = [];
    for (const { from, to } of view$1.visibleRanges) {
      language.syntaxTree(view$1.state).iterate({
        from,
        to,
        enter: ({ node }) => {
          if (/formatting/.test(node.name)) {
            return;
          }
          if (!/.*?_?inline-code_?.*/.test(node.name)) {
            return;
          }
          if (isSelectionWithin(view$1.state.selection, node.from, node.to)) {
            return;
          }
          const src = view$1.state.doc.sliceString(node.from, node.to).trim();
          const parsed = parseCode(src);
          if (!parsed) {
            return;
          }
          switch (parsed.type) {
            case "clock": {
              const { segments, filled } = parsed;
              widgets.push(view.Decoration.replace({
                widget: new ClockWidget(
                  segments,
                  filled,
                  node.from,
                  node.to,
                  this.showButtonsForInlineClocks,
                  this.allowClickInteractionForInlineClocks
                )
              }).range(node.from, node.to));
              break;
            }
            case "counter": {
              const { value } = parsed;
              widgets.push(view.Decoration.replace({
                widget: new CounterWidget(value, node.from, node.to)
              }).range(node.from, node.to));
              break;
            }
          }
        }
      });
    }
    return view.Decoration.set(widgets);
  }
}
function inlinePlugin(plugin) {
  return view.ViewPlugin.define((view2) => {
    const viewPlugin = new InlinePlugin(view2);
    viewPlugin.showButtonsForInlineClocks = plugin.settings.showButtonsForInlineClocks;
    viewPlugin.allowClickInteractionForInlineClocks = plugin.settings.allowClickInteractionForInlineClocks;
    return viewPlugin;
  }, { decorations: (view2) => view2.decorations });
}
class ProgressClocksSettingsTab extends obsidian.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    __publicField(this, "plugin");
    this.plugin = plugin;
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    new obsidian.Setting(containerEl).setName("Show Buttons for Inline Clocks").setDesc("When turned on, inline clocks will render with buttons to increment/decrement the clock, and add/remove segments from the clock. When turned off, inline clocks will render without any buttons.").addToggle(
      (toggle) => toggle.setValue(this.plugin.settings.showButtonsForInlineClocks).onChange(async (value) => {
        this.plugin.settings.showButtonsForInlineClocks = value;
        await this.plugin.saveSettings();
      })
    );
    new obsidian.Setting(containerEl).setName("Allow Click Interaction for Inline Clocks").setDesc("When turned on, inline clocks will respond to mouse clicks by adjusting the value of the clock. When turned off, the only way to update inline clocks is to edit the inline code block.").addToggle(
      (toggle) => toggle.setValue(this.plugin.settings.allowClickInteractionForInlineClocks).onChange(async (value) => {
        this.plugin.settings.allowClickInteractionForInlineClocks = value;
        await this.plugin.saveSettings();
      })
    );
  }
}
const DEFAULT_SETTINGS = {
  showButtonsForInlineClocks: true,
  allowClickInteractionForInlineClocks: true
};
class ProgressClocksPlugin extends obsidian.Plugin {
  constructor() {
    super(...arguments);
    __publicField(this, "settings");
  }
  async onload() {
    await this.loadSettings();
    this.addSettingTab(new ProgressClocksSettingsTab(this.app, this));
    this.registerView(
      VIEW_TYPE,
      (leaf) => new ProgressClocksView(this, leaf)
    );
    this.addView();
    this.addCommand({
      id: "open-panel",
      name: "Open the sidebar view",
      callback: async () => {
        const leaf = await this.addView();
        if (leaf) {
          this.app.workspace.revealLeaf(leaf);
        }
      }
    });
    this.registerEditorExtension(inlinePlugin(this));
    this.registerMarkdownPostProcessor(this.handleMarkdownPostProcessor.bind(this));
  }
  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }
  async saveSettings() {
    await this.saveData(this.settings);
  }
  async addView() {
    var _a, _b;
    if (this.app.workspace.getLeavesOfType(VIEW_TYPE).length > 0) {
      return this.app.workspace.getLeavesOfType(VIEW_TYPE)[0];
    }
    await ((_b = (_a = this.app.workspace) == null ? void 0 : _a.getRightLeaf(false)) == null ? void 0 : _b.setViewState({
      type: VIEW_TYPE
    }));
    return this.app.workspace.getLeavesOfType(VIEW_TYPE)[0];
  }
  async handleMarkdownPostProcessor(el, ctx) {
    const nodes = el.querySelectorAll("code");
    for (let i = 0; i < nodes.length; ++i) {
      const node = nodes[i];
      const parsed = parseCode(node.innerText);
      if (!parsed) {
        continue;
      }
      const container = document.createElement("div");
      container.addClass("progress-clocks-inline");
      switch (parsed.type) {
        case "clock": {
          const { segments, filled } = parsed;
          new Clock({
            target: container,
            props: {
              segments,
              filled,
              showButtonsForInlineClocks: this.settings.showButtonsForInlineClocks,
              allowClickInteractionForInlineClocks: this.settings.allowClickInteractionForInlineClocks
            }
          });
          node.replaceWith(container);
          break;
        }
        case "counter": {
          const { value } = parsed;
          new Counter({
            target: container,
            props: {
              value
            }
          });
          node.replaceWith(container);
          break;
        }
      }
    }
  }
}
module.exports = ProgressClocksPlugin;


/* nosourcemap */