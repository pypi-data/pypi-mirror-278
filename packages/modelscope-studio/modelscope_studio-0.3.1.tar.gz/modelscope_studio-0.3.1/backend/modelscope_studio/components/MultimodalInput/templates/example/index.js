const {
  SvelteComponent: E,
  append: k,
  attr: u,
  detach: F,
  init: H,
  insert: P,
  noop: v,
  safe_not_equal: V,
  svg_element: w
} = window.__gradio__svelte__internal;
function W(i) {
  let e, s, a;
  return {
    c() {
      e = w("svg"), s = w("path"), a = w("polyline"), u(s, "d", "M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"), u(a, "points", "13 2 13 9 20 9"), u(e, "xmlns", "http://www.w3.org/2000/svg"), u(e, "width", "100%"), u(e, "height", "100%"), u(e, "viewBox", "0 0 24 24"), u(e, "fill", "none"), u(e, "stroke", "currentColor"), u(e, "stroke-width", "1.5"), u(e, "stroke-linecap", "round"), u(e, "stroke-linejoin", "round"), u(e, "class", "feather feather-file");
    },
    m(r, f) {
      P(r, e, f), k(e, s), k(e, a);
    },
    p: v,
    i: v,
    o: v,
    d(r) {
      r && F(e);
    }
  };
}
class A extends E {
  constructor(e) {
    super(), H(this, e, null, W, V, {});
  }
}
const {
  SvelteComponent: D,
  add_iframe_resize_listener: G,
  add_render_callback: I,
  append: g,
  attr: b,
  binding_callbacks: J,
  check_outros: K,
  create_component: L,
  destroy_component: N,
  detach: C,
  element: h,
  group_outros: O,
  init: Q,
  insert: S,
  mount_component: R,
  safe_not_equal: T,
  set_data: q,
  space: M,
  text: B,
  toggle_class: p,
  transition_in: m,
  transition_out: y
} = window.__gradio__svelte__internal, { onMount: U } = window.__gradio__svelte__internal;
function j(i) {
  let e, s, a, r, f = (
    /*value*/
    i[0].files.map(z).join(", ") + ""
  ), _, l;
  return a = new A({}), {
    c() {
      e = h("span"), s = h("i"), L(a.$$.fragment), r = M(), _ = B(f), b(s, "class", "svelte-1j28ovu"), b(e, "class", "files svelte-1j28ovu");
    },
    m(t, c) {
      S(t, e, c), g(e, s), R(a, s, null), g(e, r), g(e, _), l = !0;
    },
    p(t, c) {
      (!l || c & /*value*/
      1) && f !== (f = /*value*/
      t[0].files.map(z).join(", ") + "") && q(_, f);
    },
    i(t) {
      l || (m(a.$$.fragment, t), l = !0);
    },
    o(t) {
      y(a.$$.fragment, t), l = !1;
    },
    d(t) {
      t && C(e), N(a);
    }
  };
}
function X(i) {
  var c;
  let e, s, a = (
    /*value*/
    i[0].text + ""
  ), r, f, _, l, t = (
    /*value*/
    ((c = i[0].files) == null ? void 0 : c.length) > 0 && j(i)
  );
  return {
    c() {
      e = h("div"), s = h("span"), r = B(a), f = M(), t && t.c(), b(e, "class", "svelte-1j28ovu"), I(() => (
        /*div_elementresize_handler*/
        i[5].call(e)
      )), p(
        e,
        "table",
        /*type*/
        i[1] === "table"
      ), p(
        e,
        "gallery",
        /*type*/
        i[1] === "gallery"
      ), p(
        e,
        "selected",
        /*selected*/
        i[2]
      );
    },
    m(o, n) {
      S(o, e, n), g(e, s), g(s, r), g(e, f), t && t.m(e, null), _ = G(
        e,
        /*div_elementresize_handler*/
        i[5].bind(e)
      ), i[6](e), l = !0;
    },
    p(o, [n]) {
      var d;
      (!l || n & /*value*/
      1) && a !== (a = /*value*/
      o[0].text + "") && q(r, a), /*value*/
      ((d = o[0].files) == null ? void 0 : d.length) > 0 ? t ? (t.p(o, n), n & /*value*/
      1 && m(t, 1)) : (t = j(o), t.c(), m(t, 1), t.m(e, null)) : t && (O(), y(t, 1, 1, () => {
        t = null;
      }), K()), (!l || n & /*type*/
      2) && p(
        e,
        "table",
        /*type*/
        o[1] === "table"
      ), (!l || n & /*type*/
      2) && p(
        e,
        "gallery",
        /*type*/
        o[1] === "gallery"
      ), (!l || n & /*selected*/
      4) && p(
        e,
        "selected",
        /*selected*/
        o[2]
      );
    },
    i(o) {
      l || (m(t), l = !0);
    },
    o(o) {
      y(t), l = !1;
    },
    d(o) {
      o && C(e), t && t.d(), _(), i[6](null);
    }
  };
}
const z = (i) => i.orig_name;
function Y(i, e, s) {
  let { value: a } = e, { type: r } = e, { selected: f = !1 } = e, _, l;
  function t(n, d) {
    !n || !d || (l.style.setProperty("--local-text-width", `${d < 150 ? d : 200}px`), s(4, l.style.whiteSpace = "unset", l));
  }
  U(() => {
    t(l, _);
  });
  function c() {
    _ = this.clientWidth, s(3, _);
  }
  function o(n) {
    J[n ? "unshift" : "push"](() => {
      l = n, s(4, l);
    });
  }
  return i.$$set = (n) => {
    "value" in n && s(0, a = n.value), "type" in n && s(1, r = n.type), "selected" in n && s(2, f = n.selected);
  }, [a, r, f, _, l, c, o];
}
class Z extends D {
  constructor(e) {
    super(), Q(this, e, Y, X, T, { value: 0, type: 1, selected: 2 });
  }
}
export {
  Z as default
};
