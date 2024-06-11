const {
  SvelteComponent: gn,
  assign: wn,
  create_slot: vn,
  detach: pn,
  element: kn,
  get_all_dirty_from_scope: yn,
  get_slot_changes: qn,
  get_spread_update: Cn,
  init: Ln,
  insert: zn,
  safe_not_equal: Sn,
  set_dynamic_element_data: Wl,
  set_style: K,
  toggle_class: re,
  transition_in: Pt,
  transition_out: Rt,
  update_slot_base: jn
} = window.__gradio__svelte__internal;
function Fn(t) {
  let e, l, n;
  const i = (
    /*#slots*/
    t[18].default
  ), o = vn(
    i,
    t,
    /*$$scope*/
    t[17],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      t[7]
    ) },
    { id: (
      /*elem_id*/
      t[2]
    ) },
    {
      class: l = "block " + /*elem_classes*/
      t[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let f = 0; f < a.length; f += 1)
    r = wn(r, a[f]);
  return {
    c() {
      e = kn(
        /*tag*/
        t[14]
      ), o && o.c(), Wl(
        /*tag*/
        t[14]
      )(e, r), re(
        e,
        "hidden",
        /*visible*/
        t[10] === !1
      ), re(
        e,
        "padded",
        /*padding*/
        t[6]
      ), re(
        e,
        "border_focus",
        /*border_mode*/
        t[5] === "focus"
      ), re(
        e,
        "border_contrast",
        /*border_mode*/
        t[5] === "contrast"
      ), re(e, "hide-container", !/*explicit_call*/
      t[8] && !/*container*/
      t[9]), K(
        e,
        "height",
        /*get_dimension*/
        t[15](
          /*height*/
          t[0]
        )
      ), K(e, "width", typeof /*width*/
      t[1] == "number" ? `calc(min(${/*width*/
      t[1]}px, 100%))` : (
        /*get_dimension*/
        t[15](
          /*width*/
          t[1]
        )
      )), K(
        e,
        "border-style",
        /*variant*/
        t[4]
      ), K(
        e,
        "overflow",
        /*allow_overflow*/
        t[11] ? "visible" : "hidden"
      ), K(
        e,
        "flex-grow",
        /*scale*/
        t[12]
      ), K(e, "min-width", `calc(min(${/*min_width*/
      t[13]}px, 100%))`), K(e, "border-width", "var(--block-border-width)");
    },
    m(f, s) {
      zn(f, e, s), o && o.m(e, null), n = !0;
    },
    p(f, s) {
      o && o.p && (!n || s & /*$$scope*/
      131072) && jn(
        o,
        i,
        f,
        /*$$scope*/
        f[17],
        n ? qn(
          i,
          /*$$scope*/
          f[17],
          s,
          null
        ) : yn(
          /*$$scope*/
          f[17]
        ),
        null
      ), Wl(
        /*tag*/
        f[14]
      )(e, r = Cn(a, [
        (!n || s & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          f[7]
        ) },
        (!n || s & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          f[2]
        ) },
        (!n || s & /*elem_classes*/
        8 && l !== (l = "block " + /*elem_classes*/
        f[3].join(" ") + " svelte-nl1om8")) && { class: l }
      ])), re(
        e,
        "hidden",
        /*visible*/
        f[10] === !1
      ), re(
        e,
        "padded",
        /*padding*/
        f[6]
      ), re(
        e,
        "border_focus",
        /*border_mode*/
        f[5] === "focus"
      ), re(
        e,
        "border_contrast",
        /*border_mode*/
        f[5] === "contrast"
      ), re(e, "hide-container", !/*explicit_call*/
      f[8] && !/*container*/
      f[9]), s & /*height*/
      1 && K(
        e,
        "height",
        /*get_dimension*/
        f[15](
          /*height*/
          f[0]
        )
      ), s & /*width*/
      2 && K(e, "width", typeof /*width*/
      f[1] == "number" ? `calc(min(${/*width*/
      f[1]}px, 100%))` : (
        /*get_dimension*/
        f[15](
          /*width*/
          f[1]
        )
      )), s & /*variant*/
      16 && K(
        e,
        "border-style",
        /*variant*/
        f[4]
      ), s & /*allow_overflow*/
      2048 && K(
        e,
        "overflow",
        /*allow_overflow*/
        f[11] ? "visible" : "hidden"
      ), s & /*scale*/
      4096 && K(
        e,
        "flex-grow",
        /*scale*/
        f[12]
      ), s & /*min_width*/
      8192 && K(e, "min-width", `calc(min(${/*min_width*/
      f[13]}px, 100%))`);
    },
    i(f) {
      n || (Pt(o, f), n = !0);
    },
    o(f) {
      Rt(o, f), n = !1;
    },
    d(f) {
      f && pn(e), o && o.d(f);
    }
  };
}
function Mn(t) {
  let e, l = (
    /*tag*/
    t[14] && Fn(t)
  );
  return {
    c() {
      l && l.c();
    },
    m(n, i) {
      l && l.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && l.p(n, i);
    },
    i(n) {
      e || (Pt(l, n), e = !0);
    },
    o(n) {
      Rt(l, n), e = !1;
    },
    d(n) {
      l && l.d(n);
    }
  };
}
function En(t, e, l) {
  let { $$slots: n = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: a = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: f = [] } = e, { variant: s = "solid" } = e, { border_mode: _ = "base" } = e, { padding: u = !0 } = e, { type: c = "normal" } = e, { test_id: d = void 0 } = e, { explicit_call: w = !1 } = e, { container: p = !0 } = e, { visible: v = !0 } = e, { allow_overflow: k = !0 } = e, { scale: h = null } = e, { min_width: b = 0 } = e, m = c === "fieldset" ? "fieldset" : "div";
  const L = (q) => {
    if (q !== void 0) {
      if (typeof q == "number")
        return q + "px";
      if (typeof q == "string")
        return q;
    }
  };
  return t.$$set = (q) => {
    "height" in q && l(0, o = q.height), "width" in q && l(1, a = q.width), "elem_id" in q && l(2, r = q.elem_id), "elem_classes" in q && l(3, f = q.elem_classes), "variant" in q && l(4, s = q.variant), "border_mode" in q && l(5, _ = q.border_mode), "padding" in q && l(6, u = q.padding), "type" in q && l(16, c = q.type), "test_id" in q && l(7, d = q.test_id), "explicit_call" in q && l(8, w = q.explicit_call), "container" in q && l(9, p = q.container), "visible" in q && l(10, v = q.visible), "allow_overflow" in q && l(11, k = q.allow_overflow), "scale" in q && l(12, h = q.scale), "min_width" in q && l(13, b = q.min_width), "$$scope" in q && l(17, i = q.$$scope);
  }, [
    o,
    a,
    r,
    f,
    s,
    _,
    u,
    d,
    w,
    p,
    v,
    k,
    h,
    b,
    m,
    L,
    c,
    i,
    n
  ];
}
class An extends gn {
  constructor(e) {
    super(), Ln(this, e, En, Mn, Sn, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: In,
  append: zl,
  attr: il,
  create_component: Bn,
  destroy_component: Dn,
  detach: Vn,
  element: Yl,
  init: Nn,
  insert: Zn,
  mount_component: Tn,
  safe_not_equal: Pn,
  set_data: Rn,
  space: On,
  text: Gn,
  toggle_class: ke,
  transition_in: Xn,
  transition_out: Hn
} = window.__gradio__svelte__internal;
function Un(t) {
  let e, l, n, i, o, a;
  return n = new /*Icon*/
  t[1]({}), {
    c() {
      e = Yl("label"), l = Yl("span"), Bn(n.$$.fragment), i = On(), o = Gn(
        /*label*/
        t[0]
      ), il(l, "class", "svelte-9gxdi0"), il(e, "for", ""), il(e, "data-testid", "block-label"), il(e, "class", "svelte-9gxdi0"), ke(e, "hide", !/*show_label*/
      t[2]), ke(e, "sr-only", !/*show_label*/
      t[2]), ke(
        e,
        "float",
        /*float*/
        t[4]
      ), ke(
        e,
        "hide-label",
        /*disable*/
        t[3]
      );
    },
    m(r, f) {
      Zn(r, e, f), zl(e, l), Tn(n, l, null), zl(e, i), zl(e, o), a = !0;
    },
    p(r, [f]) {
      (!a || f & /*label*/
      1) && Rn(
        o,
        /*label*/
        r[0]
      ), (!a || f & /*show_label*/
      4) && ke(e, "hide", !/*show_label*/
      r[2]), (!a || f & /*show_label*/
      4) && ke(e, "sr-only", !/*show_label*/
      r[2]), (!a || f & /*float*/
      16) && ke(
        e,
        "float",
        /*float*/
        r[4]
      ), (!a || f & /*disable*/
      8) && ke(
        e,
        "hide-label",
        /*disable*/
        r[3]
      );
    },
    i(r) {
      a || (Xn(n.$$.fragment, r), a = !0);
    },
    o(r) {
      Hn(n.$$.fragment, r), a = !1;
    },
    d(r) {
      r && Vn(e), Dn(n);
    }
  };
}
function Wn(t, e, l) {
  let { label: n = null } = e, { Icon: i } = e, { show_label: o = !0 } = e, { disable: a = !1 } = e, { float: r = !0 } = e;
  return t.$$set = (f) => {
    "label" in f && l(0, n = f.label), "Icon" in f && l(1, i = f.Icon), "show_label" in f && l(2, o = f.show_label), "disable" in f && l(3, a = f.disable), "float" in f && l(4, r = f.float);
  }, [n, i, o, a, r];
}
class Yn extends In {
  constructor(e) {
    super(), Nn(this, e, Wn, Un, Pn, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: Jn,
  append: Dl,
  attr: ge,
  bubble: Kn,
  create_component: Qn,
  destroy_component: xn,
  detach: Ot,
  element: Vl,
  init: $n,
  insert: Gt,
  listen: ei,
  mount_component: li,
  safe_not_equal: ti,
  set_data: ni,
  set_style: Te,
  space: ii,
  text: oi,
  toggle_class: H,
  transition_in: si,
  transition_out: fi
} = window.__gradio__svelte__internal;
function Jl(t) {
  let e, l;
  return {
    c() {
      e = Vl("span"), l = oi(
        /*label*/
        t[1]
      ), ge(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Gt(n, e, i), Dl(e, l);
    },
    p(n, i) {
      i & /*label*/
      2 && ni(
        l,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && Ot(e);
    }
  };
}
function ai(t) {
  let e, l, n, i, o, a, r, f = (
    /*show_label*/
    t[2] && Jl(t)
  );
  return i = new /*Icon*/
  t[0]({}), {
    c() {
      e = Vl("button"), f && f.c(), l = ii(), n = Vl("div"), Qn(i.$$.fragment), ge(n, "class", "svelte-1lrphxw"), H(
        n,
        "small",
        /*size*/
        t[4] === "small"
      ), H(
        n,
        "large",
        /*size*/
        t[4] === "large"
      ), H(
        n,
        "medium",
        /*size*/
        t[4] === "medium"
      ), e.disabled = /*disabled*/
      t[7], ge(
        e,
        "aria-label",
        /*label*/
        t[1]
      ), ge(
        e,
        "aria-haspopup",
        /*hasPopup*/
        t[8]
      ), ge(
        e,
        "title",
        /*label*/
        t[1]
      ), ge(e, "class", "svelte-1lrphxw"), H(
        e,
        "pending",
        /*pending*/
        t[3]
      ), H(
        e,
        "padded",
        /*padded*/
        t[5]
      ), H(
        e,
        "highlight",
        /*highlight*/
        t[6]
      ), H(
        e,
        "transparent",
        /*transparent*/
        t[9]
      ), Te(e, "color", !/*disabled*/
      t[7] && /*_color*/
      t[12] ? (
        /*_color*/
        t[12]
      ) : "var(--block-label-text-color)"), Te(e, "--bg-color", /*disabled*/
      t[7] ? "auto" : (
        /*background*/
        t[10]
      )), Te(
        e,
        "margin-left",
        /*offset*/
        t[11] + "px"
      );
    },
    m(s, _) {
      Gt(s, e, _), f && f.m(e, null), Dl(e, l), Dl(e, n), li(i, n, null), o = !0, a || (r = ei(
        e,
        "click",
        /*click_handler*/
        t[14]
      ), a = !0);
    },
    p(s, [_]) {
      /*show_label*/
      s[2] ? f ? f.p(s, _) : (f = Jl(s), f.c(), f.m(e, l)) : f && (f.d(1), f = null), (!o || _ & /*size*/
      16) && H(
        n,
        "small",
        /*size*/
        s[4] === "small"
      ), (!o || _ & /*size*/
      16) && H(
        n,
        "large",
        /*size*/
        s[4] === "large"
      ), (!o || _ & /*size*/
      16) && H(
        n,
        "medium",
        /*size*/
        s[4] === "medium"
      ), (!o || _ & /*disabled*/
      128) && (e.disabled = /*disabled*/
      s[7]), (!o || _ & /*label*/
      2) && ge(
        e,
        "aria-label",
        /*label*/
        s[1]
      ), (!o || _ & /*hasPopup*/
      256) && ge(
        e,
        "aria-haspopup",
        /*hasPopup*/
        s[8]
      ), (!o || _ & /*label*/
      2) && ge(
        e,
        "title",
        /*label*/
        s[1]
      ), (!o || _ & /*pending*/
      8) && H(
        e,
        "pending",
        /*pending*/
        s[3]
      ), (!o || _ & /*padded*/
      32) && H(
        e,
        "padded",
        /*padded*/
        s[5]
      ), (!o || _ & /*highlight*/
      64) && H(
        e,
        "highlight",
        /*highlight*/
        s[6]
      ), (!o || _ & /*transparent*/
      512) && H(
        e,
        "transparent",
        /*transparent*/
        s[9]
      ), _ & /*disabled, _color*/
      4224 && Te(e, "color", !/*disabled*/
      s[7] && /*_color*/
      s[12] ? (
        /*_color*/
        s[12]
      ) : "var(--block-label-text-color)"), _ & /*disabled, background*/
      1152 && Te(e, "--bg-color", /*disabled*/
      s[7] ? "auto" : (
        /*background*/
        s[10]
      )), _ & /*offset*/
      2048 && Te(
        e,
        "margin-left",
        /*offset*/
        s[11] + "px"
      );
    },
    i(s) {
      o || (si(i.$$.fragment, s), o = !0);
    },
    o(s) {
      fi(i.$$.fragment, s), o = !1;
    },
    d(s) {
      s && Ot(e), f && f.d(), xn(i), a = !1, r();
    }
  };
}
function ri(t, e, l) {
  let n, { Icon: i } = e, { label: o = "" } = e, { show_label: a = !1 } = e, { pending: r = !1 } = e, { size: f = "small" } = e, { padded: s = !0 } = e, { highlight: _ = !1 } = e, { disabled: u = !1 } = e, { hasPopup: c = !1 } = e, { color: d = "var(--block-label-text-color)" } = e, { transparent: w = !1 } = e, { background: p = "var(--background-fill-primary)" } = e, { offset: v = 0 } = e;
  function k(h) {
    Kn.call(this, t, h);
  }
  return t.$$set = (h) => {
    "Icon" in h && l(0, i = h.Icon), "label" in h && l(1, o = h.label), "show_label" in h && l(2, a = h.show_label), "pending" in h && l(3, r = h.pending), "size" in h && l(4, f = h.size), "padded" in h && l(5, s = h.padded), "highlight" in h && l(6, _ = h.highlight), "disabled" in h && l(7, u = h.disabled), "hasPopup" in h && l(8, c = h.hasPopup), "color" in h && l(13, d = h.color), "transparent" in h && l(9, w = h.transparent), "background" in h && l(10, p = h.background), "offset" in h && l(11, v = h.offset);
  }, t.$$.update = () => {
    t.$$.dirty & /*highlight, color*/
    8256 && l(12, n = _ ? "var(--color-accent)" : d);
  }, [
    i,
    o,
    a,
    r,
    f,
    s,
    _,
    u,
    c,
    w,
    p,
    v,
    n,
    d,
    k
  ];
}
class Xt extends Jn {
  constructor(e) {
    super(), $n(this, e, ri, ai, ti, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: _i,
  append: ui,
  attr: Sl,
  binding_callbacks: ci,
  create_slot: di,
  detach: mi,
  element: Kl,
  get_all_dirty_from_scope: hi,
  get_slot_changes: bi,
  init: gi,
  insert: wi,
  safe_not_equal: vi,
  toggle_class: ye,
  transition_in: pi,
  transition_out: ki,
  update_slot_base: yi
} = window.__gradio__svelte__internal;
function qi(t) {
  let e, l, n;
  const i = (
    /*#slots*/
    t[5].default
  ), o = di(
    i,
    t,
    /*$$scope*/
    t[4],
    null
  );
  return {
    c() {
      e = Kl("div"), l = Kl("div"), o && o.c(), Sl(l, "class", "icon svelte-3w3rth"), Sl(e, "class", "empty svelte-3w3rth"), Sl(e, "aria-label", "Empty value"), ye(
        e,
        "small",
        /*size*/
        t[0] === "small"
      ), ye(
        e,
        "large",
        /*size*/
        t[0] === "large"
      ), ye(
        e,
        "unpadded_box",
        /*unpadded_box*/
        t[1]
      ), ye(
        e,
        "small_parent",
        /*parent_height*/
        t[3]
      );
    },
    m(a, r) {
      wi(a, e, r), ui(e, l), o && o.m(l, null), t[6](e), n = !0;
    },
    p(a, [r]) {
      o && o.p && (!n || r & /*$$scope*/
      16) && yi(
        o,
        i,
        a,
        /*$$scope*/
        a[4],
        n ? bi(
          i,
          /*$$scope*/
          a[4],
          r,
          null
        ) : hi(
          /*$$scope*/
          a[4]
        ),
        null
      ), (!n || r & /*size*/
      1) && ye(
        e,
        "small",
        /*size*/
        a[0] === "small"
      ), (!n || r & /*size*/
      1) && ye(
        e,
        "large",
        /*size*/
        a[0] === "large"
      ), (!n || r & /*unpadded_box*/
      2) && ye(
        e,
        "unpadded_box",
        /*unpadded_box*/
        a[1]
      ), (!n || r & /*parent_height*/
      8) && ye(
        e,
        "small_parent",
        /*parent_height*/
        a[3]
      );
    },
    i(a) {
      n || (pi(o, a), n = !0);
    },
    o(a) {
      ki(o, a), n = !1;
    },
    d(a) {
      a && mi(e), o && o.d(a), t[6](null);
    }
  };
}
function Ci(t, e, l) {
  let n, { $$slots: i = {}, $$scope: o } = e, { size: a = "small" } = e, { unpadded_box: r = !1 } = e, f;
  function s(u) {
    var c;
    if (!u)
      return !1;
    const { height: d } = u.getBoundingClientRect(), { height: w } = ((c = u.parentElement) === null || c === void 0 ? void 0 : c.getBoundingClientRect()) || { height: d };
    return d > w + 2;
  }
  function _(u) {
    ci[u ? "unshift" : "push"](() => {
      f = u, l(2, f);
    });
  }
  return t.$$set = (u) => {
    "size" in u && l(0, a = u.size), "unpadded_box" in u && l(1, r = u.unpadded_box), "$$scope" in u && l(4, o = u.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*el*/
    4 && l(3, n = s(f));
  }, [a, r, f, n, o, i, _];
}
class Li extends _i {
  constructor(e) {
    super(), gi(this, e, Ci, qi, vi, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: zi,
  append: jl,
  attr: ne,
  detach: Si,
  init: ji,
  insert: Fi,
  noop: Fl,
  safe_not_equal: Mi,
  set_style: _e,
  svg_element: ol
} = window.__gradio__svelte__internal;
function Ei(t) {
  let e, l, n, i;
  return {
    c() {
      e = ol("svg"), l = ol("g"), n = ol("path"), i = ol("path"), ne(n, "d", "M18,6L6.087,17.913"), _e(n, "fill", "none"), _e(n, "fill-rule", "nonzero"), _e(n, "stroke-width", "2px"), ne(l, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), ne(i, "d", "M4.364,4.364L19.636,19.636"), _e(i, "fill", "none"), _e(i, "fill-rule", "nonzero"), _e(i, "stroke-width", "2px"), ne(e, "width", "100%"), ne(e, "height", "100%"), ne(e, "viewBox", "0 0 24 24"), ne(e, "version", "1.1"), ne(e, "xmlns", "http://www.w3.org/2000/svg"), ne(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), ne(e, "xml:space", "preserve"), ne(e, "stroke", "currentColor"), _e(e, "fill-rule", "evenodd"), _e(e, "clip-rule", "evenodd"), _e(e, "stroke-linecap", "round"), _e(e, "stroke-linejoin", "round");
    },
    m(o, a) {
      Fi(o, e, a), jl(e, l), jl(l, n), jl(e, i);
    },
    p: Fl,
    i: Fl,
    o: Fl,
    d(o) {
      o && Si(e);
    }
  };
}
class Ai extends zi {
  constructor(e) {
    super(), ji(this, e, null, Ei, Mi, {});
  }
}
const {
  SvelteComponent: Ii,
  append: Bi,
  attr: Ke,
  detach: Di,
  init: Vi,
  insert: Ni,
  noop: Ml,
  safe_not_equal: Zi,
  svg_element: Ql
} = window.__gradio__svelte__internal;
function Ti(t) {
  let e, l;
  return {
    c() {
      e = Ql("svg"), l = Ql("path"), Ke(l, "d", "M23,20a5,5,0,0,0-3.89,1.89L11.8,17.32a4.46,4.46,0,0,0,0-2.64l7.31-4.57A5,5,0,1,0,18,7a4.79,4.79,0,0,0,.2,1.32l-7.31,4.57a5,5,0,1,0,0,6.22l7.31,4.57A4.79,4.79,0,0,0,18,25a5,5,0,1,0,5-5ZM23,4a3,3,0,1,1-3,3A3,3,0,0,1,23,4ZM7,19a3,3,0,1,1,3-3A3,3,0,0,1,7,19Zm16,9a3,3,0,1,1,3-3A3,3,0,0,1,23,28Z"), Ke(l, "fill", "currentColor"), Ke(e, "id", "icon"), Ke(e, "xmlns", "http://www.w3.org/2000/svg"), Ke(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      Ni(n, e, i), Bi(e, l);
    },
    p: Ml,
    i: Ml,
    o: Ml,
    d(n) {
      n && Di(e);
    }
  };
}
class Pi extends Ii {
  constructor(e) {
    super(), Vi(this, e, null, Ti, Zi, {});
  }
}
const {
  SvelteComponent: Ri,
  append: El,
  attr: V,
  detach: Oi,
  init: Gi,
  insert: Xi,
  noop: Al,
  safe_not_equal: Hi,
  svg_element: sl
} = window.__gradio__svelte__internal;
function Ui(t) {
  let e, l, n, i;
  return {
    c() {
      e = sl("svg"), l = sl("rect"), n = sl("circle"), i = sl("polyline"), V(l, "x", "3"), V(l, "y", "3"), V(l, "width", "18"), V(l, "height", "18"), V(l, "rx", "2"), V(l, "ry", "2"), V(n, "cx", "8.5"), V(n, "cy", "8.5"), V(n, "r", "1.5"), V(i, "points", "21 15 16 10 5 21"), V(e, "xmlns", "http://www.w3.org/2000/svg"), V(e, "width", "100%"), V(e, "height", "100%"), V(e, "viewBox", "0 0 24 24"), V(e, "fill", "none"), V(e, "stroke", "currentColor"), V(e, "stroke-width", "1.5"), V(e, "stroke-linecap", "round"), V(e, "stroke-linejoin", "round"), V(e, "class", "feather feather-image");
    },
    m(o, a) {
      Xi(o, e, a), El(e, l), El(e, n), El(e, i);
    },
    p: Al,
    i: Al,
    o: Al,
    d(o) {
      o && Oi(e);
    }
  };
}
let Ht = class extends Ri {
  constructor(e) {
    super(), Gi(this, e, null, Ui, Hi, {});
  }
};
const Wi = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], xl = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Wi.reduce(
  (t, { color: e, primary: l, secondary: n }) => ({
    ...t,
    [e]: {
      primary: xl[e][l],
      secondary: xl[e][n]
    }
  }),
  {}
);
class Yi extends Error {
  constructor(e) {
    super(e), this.name = "ShareError";
  }
}
const {
  SvelteComponent: Ji,
  create_component: Ki,
  destroy_component: Qi,
  init: xi,
  mount_component: $i,
  safe_not_equal: eo,
  transition_in: lo,
  transition_out: to
} = window.__gradio__svelte__internal, { createEventDispatcher: no } = window.__gradio__svelte__internal;
function io(t) {
  let e, l;
  return e = new Xt({
    props: {
      Icon: Pi,
      label: (
        /*i18n*/
        t[2]("common.share")
      ),
      pending: (
        /*pending*/
        t[3]
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    t[5]
  ), {
    c() {
      Ki(e.$$.fragment);
    },
    m(n, i) {
      $i(e, n, i), l = !0;
    },
    p(n, [i]) {
      const o = {};
      i & /*i18n*/
      4 && (o.label = /*i18n*/
      n[2]("common.share")), i & /*pending*/
      8 && (o.pending = /*pending*/
      n[3]), e.$set(o);
    },
    i(n) {
      l || (lo(e.$$.fragment, n), l = !0);
    },
    o(n) {
      to(e.$$.fragment, n), l = !1;
    },
    d(n) {
      Qi(e, n);
    }
  };
}
function oo(t, e, l) {
  const n = no();
  let { formatter: i } = e, { value: o } = e, { i18n: a } = e, r = !1;
  const f = async () => {
    try {
      l(3, r = !0);
      const s = await i(o);
      n("share", { description: s });
    } catch (s) {
      console.error(s);
      let _ = s instanceof Yi ? s.message : "Share failed.";
      n("error", _);
    } finally {
      l(3, r = !1);
    }
  };
  return t.$$set = (s) => {
    "formatter" in s && l(0, i = s.formatter), "value" in s && l(1, o = s.value), "i18n" in s && l(2, a = s.i18n);
  }, [i, o, a, r, n, f];
}
class so extends Ji {
  constructor(e) {
    super(), xi(this, e, oo, io, eo, { formatter: 0, value: 1, i18n: 2 });
  }
}
function Re(t) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], l = 0;
  for (; t > 1e3 && l < e.length - 1; )
    t /= 1e3, l++;
  let n = e[l];
  return (Number.isInteger(t) ? t : t.toFixed(1)) + n;
}
function rl() {
}
function fo(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
const Ut = typeof window < "u";
let $l = Ut ? () => window.performance.now() : () => Date.now(), Wt = Ut ? (t) => requestAnimationFrame(t) : rl;
const Xe = /* @__PURE__ */ new Set();
function Yt(t) {
  Xe.forEach((e) => {
    e.c(t) || (Xe.delete(e), e.f());
  }), Xe.size !== 0 && Wt(Yt);
}
function ao(t) {
  let e;
  return Xe.size === 0 && Wt(Yt), {
    promise: new Promise((l) => {
      Xe.add(e = { c: t, f: l });
    }),
    abort() {
      Xe.delete(e);
    }
  };
}
const Pe = [];
function ro(t, e = rl) {
  let l;
  const n = /* @__PURE__ */ new Set();
  function i(r) {
    if (fo(t, r) && (t = r, l)) {
      const f = !Pe.length;
      for (const s of n)
        s[1](), Pe.push(s, t);
      if (f) {
        for (let s = 0; s < Pe.length; s += 2)
          Pe[s][0](Pe[s + 1]);
        Pe.length = 0;
      }
    }
  }
  function o(r) {
    i(r(t));
  }
  function a(r, f = rl) {
    const s = [r, f];
    return n.add(s), n.size === 1 && (l = e(i, o) || rl), r(t), () => {
      n.delete(s), n.size === 0 && l && (l(), l = null);
    };
  }
  return { set: i, update: o, subscribe: a };
}
function et(t) {
  return Object.prototype.toString.call(t) === "[object Date]";
}
function Nl(t, e, l, n) {
  if (typeof l == "number" || et(l)) {
    const i = n - l, o = (l - e) / (t.dt || 1 / 60), a = t.opts.stiffness * i, r = t.opts.damping * o, f = (a - r) * t.inv_mass, s = (o + f) * t.dt;
    return Math.abs(s) < t.opts.precision && Math.abs(i) < t.opts.precision ? n : (t.settled = !1, et(l) ? new Date(l.getTime() + s) : l + s);
  } else {
    if (Array.isArray(l))
      return l.map(
        (i, o) => Nl(t, e[o], l[o], n[o])
      );
    if (typeof l == "object") {
      const i = {};
      for (const o in l)
        i[o] = Nl(t, e[o], l[o], n[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof l} values`);
  }
}
function lt(t, e = {}) {
  const l = ro(t), { stiffness: n = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let a, r, f, s = t, _ = t, u = 1, c = 0, d = !1;
  function w(v, k = {}) {
    _ = v;
    const h = f = {};
    return t == null || k.hard || p.stiffness >= 1 && p.damping >= 1 ? (d = !0, a = $l(), s = v, l.set(t = _), Promise.resolve()) : (k.soft && (c = 1 / ((k.soft === !0 ? 0.5 : +k.soft) * 60), u = 0), r || (a = $l(), d = !1, r = ao((b) => {
      if (d)
        return d = !1, r = null, !1;
      u = Math.min(u + c, 1);
      const m = {
        inv_mass: u,
        opts: p,
        settled: !0,
        dt: (b - a) * 60 / 1e3
      }, L = Nl(m, s, t, _);
      return a = b, s = t, l.set(t = L), m.settled && (r = null), !m.settled;
    })), new Promise((b) => {
      r.promise.then(() => {
        h === f && b();
      });
    }));
  }
  const p = {
    set: w,
    update: (v, k) => w(v(_, t), k),
    subscribe: l.subscribe,
    stiffness: n,
    damping: i,
    precision: o
  };
  return p;
}
const {
  SvelteComponent: _o,
  append: ie,
  attr: M,
  component_subscribe: tt,
  detach: uo,
  element: co,
  init: mo,
  insert: ho,
  noop: nt,
  safe_not_equal: bo,
  set_style: fl,
  svg_element: oe,
  toggle_class: it
} = window.__gradio__svelte__internal, { onMount: go } = window.__gradio__svelte__internal;
function wo(t) {
  let e, l, n, i, o, a, r, f, s, _, u, c;
  return {
    c() {
      e = co("div"), l = oe("svg"), n = oe("g"), i = oe("path"), o = oe("path"), a = oe("path"), r = oe("path"), f = oe("g"), s = oe("path"), _ = oe("path"), u = oe("path"), c = oe("path"), M(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), M(i, "fill", "#FF7C00"), M(i, "fill-opacity", "0.4"), M(i, "class", "svelte-43sxxs"), M(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), M(o, "fill", "#FF7C00"), M(o, "class", "svelte-43sxxs"), M(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), M(a, "fill", "#FF7C00"), M(a, "fill-opacity", "0.4"), M(a, "class", "svelte-43sxxs"), M(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), M(r, "fill", "#FF7C00"), M(r, "class", "svelte-43sxxs"), fl(n, "transform", "translate(" + /*$top*/
      t[1][0] + "px, " + /*$top*/
      t[1][1] + "px)"), M(s, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), M(s, "fill", "#FF7C00"), M(s, "fill-opacity", "0.4"), M(s, "class", "svelte-43sxxs"), M(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), M(_, "fill", "#FF7C00"), M(_, "class", "svelte-43sxxs"), M(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), M(u, "fill", "#FF7C00"), M(u, "fill-opacity", "0.4"), M(u, "class", "svelte-43sxxs"), M(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), M(c, "fill", "#FF7C00"), M(c, "class", "svelte-43sxxs"), fl(f, "transform", "translate(" + /*$bottom*/
      t[2][0] + "px, " + /*$bottom*/
      t[2][1] + "px)"), M(l, "viewBox", "-1200 -1200 3000 3000"), M(l, "fill", "none"), M(l, "xmlns", "http://www.w3.org/2000/svg"), M(l, "class", "svelte-43sxxs"), M(e, "class", "svelte-43sxxs"), it(
        e,
        "margin",
        /*margin*/
        t[0]
      );
    },
    m(d, w) {
      ho(d, e, w), ie(e, l), ie(l, n), ie(n, i), ie(n, o), ie(n, a), ie(n, r), ie(l, f), ie(f, s), ie(f, _), ie(f, u), ie(f, c);
    },
    p(d, [w]) {
      w & /*$top*/
      2 && fl(n, "transform", "translate(" + /*$top*/
      d[1][0] + "px, " + /*$top*/
      d[1][1] + "px)"), w & /*$bottom*/
      4 && fl(f, "transform", "translate(" + /*$bottom*/
      d[2][0] + "px, " + /*$bottom*/
      d[2][1] + "px)"), w & /*margin*/
      1 && it(
        e,
        "margin",
        /*margin*/
        d[0]
      );
    },
    i: nt,
    o: nt,
    d(d) {
      d && uo(e);
    }
  };
}
function vo(t, e, l) {
  let n, i;
  var o = this && this.__awaiter || function(d, w, p, v) {
    function k(h) {
      return h instanceof p ? h : new p(function(b) {
        b(h);
      });
    }
    return new (p || (p = Promise))(function(h, b) {
      function m(F) {
        try {
          q(v.next(F));
        } catch (Z) {
          b(Z);
        }
      }
      function L(F) {
        try {
          q(v.throw(F));
        } catch (Z) {
          b(Z);
        }
      }
      function q(F) {
        F.done ? h(F.value) : k(F.value).then(m, L);
      }
      q((v = v.apply(d, w || [])).next());
    });
  };
  let { margin: a = !0 } = e;
  const r = lt([0, 0]);
  tt(t, r, (d) => l(1, n = d));
  const f = lt([0, 0]);
  tt(t, f, (d) => l(2, i = d));
  let s;
  function _() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), f.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), f.set([125, -140])]), yield Promise.all([r.set([-125, 0]), f.set([125, -0])]), yield Promise.all([r.set([125, 0]), f.set([-125, 0])]);
    });
  }
  function u() {
    return o(this, void 0, void 0, function* () {
      yield _(), s || u();
    });
  }
  function c() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), f.set([-125, 0])]), u();
    });
  }
  return go(() => (c(), () => s = !0)), t.$$set = (d) => {
    "margin" in d && l(0, a = d.margin);
  }, [a, n, i, r, f];
}
class Jt extends _o {
  constructor(e) {
    super(), mo(this, e, vo, wo, bo, { margin: 0 });
  }
}
const {
  SvelteComponent: po,
  append: Ae,
  attr: fe,
  binding_callbacks: ot,
  check_outros: Zl,
  create_component: Kt,
  create_slot: Qt,
  destroy_component: xt,
  destroy_each: $t,
  detach: z,
  element: ue,
  empty: He,
  ensure_array_like: ul,
  get_all_dirty_from_scope: en,
  get_slot_changes: ln,
  group_outros: Tl,
  init: ko,
  insert: S,
  mount_component: tn,
  noop: Pl,
  safe_not_equal: yo,
  set_data: le,
  set_style: Ce,
  space: ee,
  text: I,
  toggle_class: x,
  transition_in: se,
  transition_out: ce,
  update_slot_base: nn
} = window.__gradio__svelte__internal, { tick: qo } = window.__gradio__svelte__internal, { onDestroy: Co } = window.__gradio__svelte__internal, { createEventDispatcher: Lo } = window.__gradio__svelte__internal, zo = (t) => ({}), st = (t) => ({}), So = (t) => ({}), ft = (t) => ({});
function at(t, e, l) {
  const n = t.slice();
  return n[41] = e[l], n[43] = l, n;
}
function rt(t, e, l) {
  const n = t.slice();
  return n[41] = e[l], n;
}
function jo(t) {
  let e, l, n, i, o = (
    /*i18n*/
    t[1]("common.error") + ""
  ), a, r, f;
  l = new Xt({
    props: {
      Icon: Ai,
      label: (
        /*i18n*/
        t[1]("common.clear")
      ),
      disabled: !1
    }
  }), l.$on(
    "click",
    /*click_handler*/
    t[32]
  );
  const s = (
    /*#slots*/
    t[30].error
  ), _ = Qt(
    s,
    t,
    /*$$scope*/
    t[29],
    st
  );
  return {
    c() {
      e = ue("div"), Kt(l.$$.fragment), n = ee(), i = ue("span"), a = I(o), r = ee(), _ && _.c(), fe(e, "class", "clear-status svelte-vopvsi"), fe(i, "class", "error svelte-vopvsi");
    },
    m(u, c) {
      S(u, e, c), tn(l, e, null), S(u, n, c), S(u, i, c), Ae(i, a), S(u, r, c), _ && _.m(u, c), f = !0;
    },
    p(u, c) {
      const d = {};
      c[0] & /*i18n*/
      2 && (d.label = /*i18n*/
      u[1]("common.clear")), l.$set(d), (!f || c[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      u[1]("common.error") + "") && le(a, o), _ && _.p && (!f || c[0] & /*$$scope*/
      536870912) && nn(
        _,
        s,
        u,
        /*$$scope*/
        u[29],
        f ? ln(
          s,
          /*$$scope*/
          u[29],
          c,
          zo
        ) : en(
          /*$$scope*/
          u[29]
        ),
        st
      );
    },
    i(u) {
      f || (se(l.$$.fragment, u), se(_, u), f = !0);
    },
    o(u) {
      ce(l.$$.fragment, u), ce(_, u), f = !1;
    },
    d(u) {
      u && (z(e), z(n), z(i), z(r)), xt(l), _ && _.d(u);
    }
  };
}
function Fo(t) {
  let e, l, n, i, o, a, r, f, s, _ = (
    /*variant*/
    t[8] === "default" && /*show_eta_bar*/
    t[18] && /*show_progress*/
    t[6] === "full" && _t(t)
  );
  function u(b, m) {
    if (
      /*progress*/
      b[7]
    )
      return Ao;
    if (
      /*queue_position*/
      b[2] !== null && /*queue_size*/
      b[3] !== void 0 && /*queue_position*/
      b[2] >= 0
    )
      return Eo;
    if (
      /*queue_position*/
      b[2] === 0
    )
      return Mo;
  }
  let c = u(t), d = c && c(t), w = (
    /*timer*/
    t[5] && dt(t)
  );
  const p = [Vo, Do], v = [];
  function k(b, m) {
    return (
      /*last_progress_level*/
      b[15] != null ? 0 : (
        /*show_progress*/
        b[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = k(t)) && (a = v[o] = p[o](t));
  let h = !/*timer*/
  t[5] && pt(t);
  return {
    c() {
      _ && _.c(), e = ee(), l = ue("div"), d && d.c(), n = ee(), w && w.c(), i = ee(), a && a.c(), r = ee(), h && h.c(), f = He(), fe(l, "class", "progress-text svelte-vopvsi"), x(
        l,
        "meta-text-center",
        /*variant*/
        t[8] === "center"
      ), x(
        l,
        "meta-text",
        /*variant*/
        t[8] === "default"
      );
    },
    m(b, m) {
      _ && _.m(b, m), S(b, e, m), S(b, l, m), d && d.m(l, null), Ae(l, n), w && w.m(l, null), S(b, i, m), ~o && v[o].m(b, m), S(b, r, m), h && h.m(b, m), S(b, f, m), s = !0;
    },
    p(b, m) {
      /*variant*/
      b[8] === "default" && /*show_eta_bar*/
      b[18] && /*show_progress*/
      b[6] === "full" ? _ ? _.p(b, m) : (_ = _t(b), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), c === (c = u(b)) && d ? d.p(b, m) : (d && d.d(1), d = c && c(b), d && (d.c(), d.m(l, n))), /*timer*/
      b[5] ? w ? w.p(b, m) : (w = dt(b), w.c(), w.m(l, null)) : w && (w.d(1), w = null), (!s || m[0] & /*variant*/
      256) && x(
        l,
        "meta-text-center",
        /*variant*/
        b[8] === "center"
      ), (!s || m[0] & /*variant*/
      256) && x(
        l,
        "meta-text",
        /*variant*/
        b[8] === "default"
      );
      let L = o;
      o = k(b), o === L ? ~o && v[o].p(b, m) : (a && (Tl(), ce(v[L], 1, 1, () => {
        v[L] = null;
      }), Zl()), ~o ? (a = v[o], a ? a.p(b, m) : (a = v[o] = p[o](b), a.c()), se(a, 1), a.m(r.parentNode, r)) : a = null), /*timer*/
      b[5] ? h && (Tl(), ce(h, 1, 1, () => {
        h = null;
      }), Zl()) : h ? (h.p(b, m), m[0] & /*timer*/
      32 && se(h, 1)) : (h = pt(b), h.c(), se(h, 1), h.m(f.parentNode, f));
    },
    i(b) {
      s || (se(a), se(h), s = !0);
    },
    o(b) {
      ce(a), ce(h), s = !1;
    },
    d(b) {
      b && (z(e), z(l), z(i), z(r), z(f)), _ && _.d(b), d && d.d(), w && w.d(), ~o && v[o].d(b), h && h.d(b);
    }
  };
}
function _t(t) {
  let e, l = `translateX(${/*eta_level*/
  (t[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = ue("div"), fe(e, "class", "eta-bar svelte-vopvsi"), Ce(e, "transform", l);
    },
    m(n, i) {
      S(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && l !== (l = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && Ce(e, "transform", l);
    },
    d(n) {
      n && z(e);
    }
  };
}
function Mo(t) {
  let e;
  return {
    c() {
      e = I("processing |");
    },
    m(l, n) {
      S(l, e, n);
    },
    p: Pl,
    d(l) {
      l && z(e);
    }
  };
}
function Eo(t) {
  let e, l = (
    /*queue_position*/
    t[2] + 1 + ""
  ), n, i, o, a;
  return {
    c() {
      e = I("queue: "), n = I(l), i = I("/"), o = I(
        /*queue_size*/
        t[3]
      ), a = I(" |");
    },
    m(r, f) {
      S(r, e, f), S(r, n, f), S(r, i, f), S(r, o, f), S(r, a, f);
    },
    p(r, f) {
      f[0] & /*queue_position*/
      4 && l !== (l = /*queue_position*/
      r[2] + 1 + "") && le(n, l), f[0] & /*queue_size*/
      8 && le(
        o,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (z(e), z(n), z(i), z(o), z(a));
    }
  };
}
function Ao(t) {
  let e, l = ul(
    /*progress*/
    t[7]
  ), n = [];
  for (let i = 0; i < l.length; i += 1)
    n[i] = ct(rt(t, l, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = He();
    },
    m(i, o) {
      for (let a = 0; a < n.length; a += 1)
        n[a] && n[a].m(i, o);
      S(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        l = ul(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < l.length; a += 1) {
          const r = rt(i, l, a);
          n[a] ? n[a].p(r, o) : (n[a] = ct(r), n[a].c(), n[a].m(e.parentNode, e));
        }
        for (; a < n.length; a += 1)
          n[a].d(1);
        n.length = l.length;
      }
    },
    d(i) {
      i && z(e), $t(n, i);
    }
  };
}
function ut(t) {
  let e, l = (
    /*p*/
    t[41].unit + ""
  ), n, i, o = " ", a;
  function r(_, u) {
    return (
      /*p*/
      _[41].length != null ? Bo : Io
    );
  }
  let f = r(t), s = f(t);
  return {
    c() {
      s.c(), e = ee(), n = I(l), i = I(" | "), a = I(o);
    },
    m(_, u) {
      s.m(_, u), S(_, e, u), S(_, n, u), S(_, i, u), S(_, a, u);
    },
    p(_, u) {
      f === (f = r(_)) && s ? s.p(_, u) : (s.d(1), s = f(_), s && (s.c(), s.m(e.parentNode, e))), u[0] & /*progress*/
      128 && l !== (l = /*p*/
      _[41].unit + "") && le(n, l);
    },
    d(_) {
      _ && (z(e), z(n), z(i), z(a)), s.d(_);
    }
  };
}
function Io(t) {
  let e = Re(
    /*p*/
    t[41].index || 0
  ) + "", l;
  return {
    c() {
      l = I(e);
    },
    m(n, i) {
      S(n, l, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = Re(
        /*p*/
        n[41].index || 0
      ) + "") && le(l, e);
    },
    d(n) {
      n && z(l);
    }
  };
}
function Bo(t) {
  let e = Re(
    /*p*/
    t[41].index || 0
  ) + "", l, n, i = Re(
    /*p*/
    t[41].length
  ) + "", o;
  return {
    c() {
      l = I(e), n = I("/"), o = I(i);
    },
    m(a, r) {
      S(a, l, r), S(a, n, r), S(a, o, r);
    },
    p(a, r) {
      r[0] & /*progress*/
      128 && e !== (e = Re(
        /*p*/
        a[41].index || 0
      ) + "") && le(l, e), r[0] & /*progress*/
      128 && i !== (i = Re(
        /*p*/
        a[41].length
      ) + "") && le(o, i);
    },
    d(a) {
      a && (z(l), z(n), z(o));
    }
  };
}
function ct(t) {
  let e, l = (
    /*p*/
    t[41].index != null && ut(t)
  );
  return {
    c() {
      l && l.c(), e = He();
    },
    m(n, i) {
      l && l.m(n, i), S(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? l ? l.p(n, i) : (l = ut(n), l.c(), l.m(e.parentNode, e)) : l && (l.d(1), l = null);
    },
    d(n) {
      n && z(e), l && l.d(n);
    }
  };
}
function dt(t) {
  let e, l = (
    /*eta*/
    t[0] ? `/${/*formatted_eta*/
    t[19]}` : ""
  ), n, i;
  return {
    c() {
      e = I(
        /*formatted_timer*/
        t[20]
      ), n = I(l), i = I("s");
    },
    m(o, a) {
      S(o, e, a), S(o, n, a), S(o, i, a);
    },
    p(o, a) {
      a[0] & /*formatted_timer*/
      1048576 && le(
        e,
        /*formatted_timer*/
        o[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && l !== (l = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && le(n, l);
    },
    d(o) {
      o && (z(e), z(n), z(i));
    }
  };
}
function Do(t) {
  let e, l;
  return e = new Jt({
    props: { margin: (
      /*variant*/
      t[8] === "default"
    ) }
  }), {
    c() {
      Kt(e.$$.fragment);
    },
    m(n, i) {
      tn(e, n, i), l = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      n[8] === "default"), e.$set(o);
    },
    i(n) {
      l || (se(e.$$.fragment, n), l = !0);
    },
    o(n) {
      ce(e.$$.fragment, n), l = !1;
    },
    d(n) {
      xt(e, n);
    }
  };
}
function Vo(t) {
  let e, l, n, i, o, a = `${/*last_progress_level*/
  t[15] * 100}%`, r = (
    /*progress*/
    t[7] != null && mt(t)
  );
  return {
    c() {
      e = ue("div"), l = ue("div"), r && r.c(), n = ee(), i = ue("div"), o = ue("div"), fe(l, "class", "progress-level-inner svelte-vopvsi"), fe(o, "class", "progress-bar svelte-vopvsi"), Ce(o, "width", a), fe(i, "class", "progress-bar-wrap svelte-vopvsi"), fe(e, "class", "progress-level svelte-vopvsi");
    },
    m(f, s) {
      S(f, e, s), Ae(e, l), r && r.m(l, null), Ae(e, n), Ae(e, i), Ae(i, o), t[31](o);
    },
    p(f, s) {
      /*progress*/
      f[7] != null ? r ? r.p(f, s) : (r = mt(f), r.c(), r.m(l, null)) : r && (r.d(1), r = null), s[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      f[15] * 100}%`) && Ce(o, "width", a);
    },
    i: Pl,
    o: Pl,
    d(f) {
      f && z(e), r && r.d(), t[31](null);
    }
  };
}
function mt(t) {
  let e, l = ul(
    /*progress*/
    t[7]
  ), n = [];
  for (let i = 0; i < l.length; i += 1)
    n[i] = vt(at(t, l, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = He();
    },
    m(i, o) {
      for (let a = 0; a < n.length; a += 1)
        n[a] && n[a].m(i, o);
      S(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        l = ul(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < l.length; a += 1) {
          const r = at(i, l, a);
          n[a] ? n[a].p(r, o) : (n[a] = vt(r), n[a].c(), n[a].m(e.parentNode, e));
        }
        for (; a < n.length; a += 1)
          n[a].d(1);
        n.length = l.length;
      }
    },
    d(i) {
      i && z(e), $t(n, i);
    }
  };
}
function ht(t) {
  let e, l, n, i, o = (
    /*i*/
    t[43] !== 0 && No()
  ), a = (
    /*p*/
    t[41].desc != null && bt(t)
  ), r = (
    /*p*/
    t[41].desc != null && /*progress_level*/
    t[14] && /*progress_level*/
    t[14][
      /*i*/
      t[43]
    ] != null && gt()
  ), f = (
    /*progress_level*/
    t[14] != null && wt(t)
  );
  return {
    c() {
      o && o.c(), e = ee(), a && a.c(), l = ee(), r && r.c(), n = ee(), f && f.c(), i = He();
    },
    m(s, _) {
      o && o.m(s, _), S(s, e, _), a && a.m(s, _), S(s, l, _), r && r.m(s, _), S(s, n, _), f && f.m(s, _), S(s, i, _);
    },
    p(s, _) {
      /*p*/
      s[41].desc != null ? a ? a.p(s, _) : (a = bt(s), a.c(), a.m(l.parentNode, l)) : a && (a.d(1), a = null), /*p*/
      s[41].desc != null && /*progress_level*/
      s[14] && /*progress_level*/
      s[14][
        /*i*/
        s[43]
      ] != null ? r || (r = gt(), r.c(), r.m(n.parentNode, n)) : r && (r.d(1), r = null), /*progress_level*/
      s[14] != null ? f ? f.p(s, _) : (f = wt(s), f.c(), f.m(i.parentNode, i)) : f && (f.d(1), f = null);
    },
    d(s) {
      s && (z(e), z(l), z(n), z(i)), o && o.d(s), a && a.d(s), r && r.d(s), f && f.d(s);
    }
  };
}
function No(t) {
  let e;
  return {
    c() {
      e = I(" /");
    },
    m(l, n) {
      S(l, e, n);
    },
    d(l) {
      l && z(e);
    }
  };
}
function bt(t) {
  let e = (
    /*p*/
    t[41].desc + ""
  ), l;
  return {
    c() {
      l = I(e);
    },
    m(n, i) {
      S(n, l, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && le(l, e);
    },
    d(n) {
      n && z(l);
    }
  };
}
function gt(t) {
  let e;
  return {
    c() {
      e = I("-");
    },
    m(l, n) {
      S(l, e, n);
    },
    d(l) {
      l && z(e);
    }
  };
}
function wt(t) {
  let e = (100 * /*progress_level*/
  (t[14][
    /*i*/
    t[43]
  ] || 0)).toFixed(1) + "", l, n;
  return {
    c() {
      l = I(e), n = I("%");
    },
    m(i, o) {
      S(i, l, o), S(i, n, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && le(l, e);
    },
    d(i) {
      i && (z(l), z(n));
    }
  };
}
function vt(t) {
  let e, l = (
    /*p*/
    (t[41].desc != null || /*progress_level*/
    t[14] && /*progress_level*/
    t[14][
      /*i*/
      t[43]
    ] != null) && ht(t)
  );
  return {
    c() {
      l && l.c(), e = He();
    },
    m(n, i) {
      l && l.m(n, i), S(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? l ? l.p(n, i) : (l = ht(n), l.c(), l.m(e.parentNode, e)) : l && (l.d(1), l = null);
    },
    d(n) {
      n && z(e), l && l.d(n);
    }
  };
}
function pt(t) {
  let e, l, n, i;
  const o = (
    /*#slots*/
    t[30]["additional-loading-text"]
  ), a = Qt(
    o,
    t,
    /*$$scope*/
    t[29],
    ft
  );
  return {
    c() {
      e = ue("p"), l = I(
        /*loading_text*/
        t[9]
      ), n = ee(), a && a.c(), fe(e, "class", "loading svelte-vopvsi");
    },
    m(r, f) {
      S(r, e, f), Ae(e, l), S(r, n, f), a && a.m(r, f), i = !0;
    },
    p(r, f) {
      (!i || f[0] & /*loading_text*/
      512) && le(
        l,
        /*loading_text*/
        r[9]
      ), a && a.p && (!i || f[0] & /*$$scope*/
      536870912) && nn(
        a,
        o,
        r,
        /*$$scope*/
        r[29],
        i ? ln(
          o,
          /*$$scope*/
          r[29],
          f,
          So
        ) : en(
          /*$$scope*/
          r[29]
        ),
        ft
      );
    },
    i(r) {
      i || (se(a, r), i = !0);
    },
    o(r) {
      ce(a, r), i = !1;
    },
    d(r) {
      r && (z(e), z(n)), a && a.d(r);
    }
  };
}
function Zo(t) {
  let e, l, n, i, o;
  const a = [Fo, jo], r = [];
  function f(s, _) {
    return (
      /*status*/
      s[4] === "pending" ? 0 : (
        /*status*/
        s[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(l = f(t)) && (n = r[l] = a[l](t)), {
    c() {
      e = ue("div"), n && n.c(), fe(e, "class", i = "wrap " + /*variant*/
      t[8] + " " + /*show_progress*/
      t[6] + " svelte-vopvsi"), x(e, "hide", !/*status*/
      t[4] || /*status*/
      t[4] === "complete" || /*show_progress*/
      t[6] === "hidden"), x(
        e,
        "translucent",
        /*variant*/
        t[8] === "center" && /*status*/
        (t[4] === "pending" || /*status*/
        t[4] === "error") || /*translucent*/
        t[11] || /*show_progress*/
        t[6] === "minimal"
      ), x(
        e,
        "generating",
        /*status*/
        t[4] === "generating"
      ), x(
        e,
        "border",
        /*border*/
        t[12]
      ), Ce(
        e,
        "position",
        /*absolute*/
        t[10] ? "absolute" : "static"
      ), Ce(
        e,
        "padding",
        /*absolute*/
        t[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(s, _) {
      S(s, e, _), ~l && r[l].m(e, null), t[33](e), o = !0;
    },
    p(s, _) {
      let u = l;
      l = f(s), l === u ? ~l && r[l].p(s, _) : (n && (Tl(), ce(r[u], 1, 1, () => {
        r[u] = null;
      }), Zl()), ~l ? (n = r[l], n ? n.p(s, _) : (n = r[l] = a[l](s), n.c()), se(n, 1), n.m(e, null)) : n = null), (!o || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      s[8] + " " + /*show_progress*/
      s[6] + " svelte-vopvsi")) && fe(e, "class", i), (!o || _[0] & /*variant, show_progress, status, show_progress*/
      336) && x(e, "hide", !/*status*/
      s[4] || /*status*/
      s[4] === "complete" || /*show_progress*/
      s[6] === "hidden"), (!o || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && x(
        e,
        "translucent",
        /*variant*/
        s[8] === "center" && /*status*/
        (s[4] === "pending" || /*status*/
        s[4] === "error") || /*translucent*/
        s[11] || /*show_progress*/
        s[6] === "minimal"
      ), (!o || _[0] & /*variant, show_progress, status*/
      336) && x(
        e,
        "generating",
        /*status*/
        s[4] === "generating"
      ), (!o || _[0] & /*variant, show_progress, border*/
      4416) && x(
        e,
        "border",
        /*border*/
        s[12]
      ), _[0] & /*absolute*/
      1024 && Ce(
        e,
        "position",
        /*absolute*/
        s[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && Ce(
        e,
        "padding",
        /*absolute*/
        s[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(s) {
      o || (se(n), o = !0);
    },
    o(s) {
      ce(n), o = !1;
    },
    d(s) {
      s && z(e), ~l && r[l].d(), t[33](null);
    }
  };
}
var To = function(t, e, l, n) {
  function i(o) {
    return o instanceof l ? o : new l(function(a) {
      a(o);
    });
  }
  return new (l || (l = Promise))(function(o, a) {
    function r(_) {
      try {
        s(n.next(_));
      } catch (u) {
        a(u);
      }
    }
    function f(_) {
      try {
        s(n.throw(_));
      } catch (u) {
        a(u);
      }
    }
    function s(_) {
      _.done ? o(_.value) : i(_.value).then(r, f);
    }
    s((n = n.apply(t, e || [])).next());
  });
};
let al = [], Il = !1;
function Po(t) {
  return To(this, arguments, void 0, function* (e, l = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && l !== !0)) {
      if (al.push(e), !Il)
        Il = !0;
      else
        return;
      yield qo(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < al.length; i++) {
          const a = al[i].getBoundingClientRect();
          (i === 0 || a.top + window.scrollY <= n[0]) && (n[0] = a.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Il = !1, al = [];
      });
    }
  });
}
function Ro(t, e, l) {
  let n, { $$slots: i = {}, $$scope: o } = e;
  this && this.__awaiter;
  const a = Lo();
  let { i18n: r } = e, { eta: f = null } = e, { queue_position: s } = e, { queue_size: _ } = e, { status: u } = e, { scroll_to_output: c = !1 } = e, { timer: d = !0 } = e, { show_progress: w = "full" } = e, { message: p = null } = e, { progress: v = null } = e, { variant: k = "default" } = e, { loading_text: h = "Loading..." } = e, { absolute: b = !0 } = e, { translucent: m = !1 } = e, { border: L = !1 } = e, { autoscroll: q } = e, F, Z = !1, j = 0, D = 0, P = null, G = null, ze = 0, Y = null, J, R = null, B = !0;
  const Se = () => {
    l(0, f = l(27, P = l(19, he = null))), l(25, j = performance.now()), l(26, D = 0), Z = !0, ve();
  };
  function ve() {
    requestAnimationFrame(() => {
      l(26, D = (performance.now() - j) / 1e3), Z && ve();
    });
  }
  function je() {
    l(26, D = 0), l(0, f = l(27, P = l(19, he = null))), Z && (Z = !1);
  }
  Co(() => {
    Z && je();
  });
  let he = null;
  function y(C) {
    ot[C ? "unshift" : "push"](() => {
      R = C, l(16, R), l(7, v), l(14, Y), l(15, J);
    });
  }
  const pe = () => {
    a("clear_status");
  };
  function ae(C) {
    ot[C ? "unshift" : "push"](() => {
      F = C, l(13, F);
    });
  }
  return t.$$set = (C) => {
    "i18n" in C && l(1, r = C.i18n), "eta" in C && l(0, f = C.eta), "queue_position" in C && l(2, s = C.queue_position), "queue_size" in C && l(3, _ = C.queue_size), "status" in C && l(4, u = C.status), "scroll_to_output" in C && l(22, c = C.scroll_to_output), "timer" in C && l(5, d = C.timer), "show_progress" in C && l(6, w = C.show_progress), "message" in C && l(23, p = C.message), "progress" in C && l(7, v = C.progress), "variant" in C && l(8, k = C.variant), "loading_text" in C && l(9, h = C.loading_text), "absolute" in C && l(10, b = C.absolute), "translucent" in C && l(11, m = C.translucent), "border" in C && l(12, L = C.border), "autoscroll" in C && l(24, q = C.autoscroll), "$$scope" in C && l(29, o = C.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (f === null && l(0, f = P), f != null && P !== f && (l(28, G = (performance.now() - j) / 1e3 + f), l(19, he = G.toFixed(1)), l(27, P = f))), t.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && l(17, ze = G === null || G <= 0 || !D ? null : Math.min(D / G, 1)), t.$$.dirty[0] & /*progress*/
    128 && v != null && l(18, B = !1), t.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (v != null ? l(14, Y = v.map((C) => {
      if (C.index != null && C.length != null)
        return C.index / C.length;
      if (C.progress != null)
        return C.progress;
    })) : l(14, Y = null), Y ? (l(15, J = Y[Y.length - 1]), R && (J === 0 ? l(16, R.style.transition = "0", R) : l(16, R.style.transition = "150ms", R))) : l(15, J = void 0)), t.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? Se() : je()), t.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && F && c && (u === "pending" || u === "complete") && Po(F, q), t.$$.dirty[0] & /*status, message*/
    8388624, t.$$.dirty[0] & /*timer_diff*/
    67108864 && l(20, n = D.toFixed(1));
  }, [
    f,
    r,
    s,
    _,
    u,
    d,
    w,
    v,
    k,
    h,
    b,
    m,
    L,
    F,
    Y,
    J,
    R,
    ze,
    B,
    he,
    n,
    a,
    c,
    p,
    q,
    j,
    D,
    P,
    G,
    o,
    i,
    y,
    pe,
    ae
  ];
}
class Oo extends po {
  constructor(e) {
    super(), ko(
      this,
      e,
      Ro,
      Zo,
      yo,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Go,
  append: on,
  attr: A,
  bubble: Xo,
  check_outros: Ho,
  create_slot: sn,
  detach: ll,
  element: vl,
  empty: Uo,
  get_all_dirty_from_scope: fn,
  get_slot_changes: an,
  group_outros: Wo,
  init: Yo,
  insert: tl,
  listen: Jo,
  safe_not_equal: Ko,
  set_style: U,
  space: rn,
  src_url_equal: cl,
  toggle_class: Oe,
  transition_in: dl,
  transition_out: ml,
  update_slot_base: _n
} = window.__gradio__svelte__internal;
function Qo(t) {
  let e, l, n, i, o, a, r = (
    /*icon*/
    t[7] && kt(t)
  );
  const f = (
    /*#slots*/
    t[12].default
  ), s = sn(
    f,
    t,
    /*$$scope*/
    t[11],
    null
  );
  return {
    c() {
      e = vl("button"), r && r.c(), l = rn(), s && s.c(), A(e, "class", n = /*size*/
      t[4] + " " + /*variant*/
      t[3] + " " + /*elem_classes*/
      t[1].join(" ") + " svelte-8huxfn"), A(
        e,
        "id",
        /*elem_id*/
        t[0]
      ), e.disabled = /*disabled*/
      t[8], Oe(e, "hidden", !/*visible*/
      t[2]), U(
        e,
        "flex-grow",
        /*scale*/
        t[9]
      ), U(
        e,
        "width",
        /*scale*/
        t[9] === 0 ? "fit-content" : null
      ), U(e, "min-width", typeof /*min_width*/
      t[10] == "number" ? `calc(min(${/*min_width*/
      t[10]}px, 100%))` : null);
    },
    m(_, u) {
      tl(_, e, u), r && r.m(e, null), on(e, l), s && s.m(e, null), i = !0, o || (a = Jo(
        e,
        "click",
        /*click_handler*/
        t[13]
      ), o = !0);
    },
    p(_, u) {
      /*icon*/
      _[7] ? r ? r.p(_, u) : (r = kt(_), r.c(), r.m(e, l)) : r && (r.d(1), r = null), s && s.p && (!i || u & /*$$scope*/
      2048) && _n(
        s,
        f,
        _,
        /*$$scope*/
        _[11],
        i ? an(
          f,
          /*$$scope*/
          _[11],
          u,
          null
        ) : fn(
          /*$$scope*/
          _[11]
        ),
        null
      ), (!i || u & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      _[4] + " " + /*variant*/
      _[3] + " " + /*elem_classes*/
      _[1].join(" ") + " svelte-8huxfn")) && A(e, "class", n), (!i || u & /*elem_id*/
      1) && A(
        e,
        "id",
        /*elem_id*/
        _[0]
      ), (!i || u & /*disabled*/
      256) && (e.disabled = /*disabled*/
      _[8]), (!i || u & /*size, variant, elem_classes, visible*/
      30) && Oe(e, "hidden", !/*visible*/
      _[2]), u & /*scale*/
      512 && U(
        e,
        "flex-grow",
        /*scale*/
        _[9]
      ), u & /*scale*/
      512 && U(
        e,
        "width",
        /*scale*/
        _[9] === 0 ? "fit-content" : null
      ), u & /*min_width*/
      1024 && U(e, "min-width", typeof /*min_width*/
      _[10] == "number" ? `calc(min(${/*min_width*/
      _[10]}px, 100%))` : null);
    },
    i(_) {
      i || (dl(s, _), i = !0);
    },
    o(_) {
      ml(s, _), i = !1;
    },
    d(_) {
      _ && ll(e), r && r.d(), s && s.d(_), o = !1, a();
    }
  };
}
function xo(t) {
  let e, l, n, i, o = (
    /*icon*/
    t[7] && yt(t)
  );
  const a = (
    /*#slots*/
    t[12].default
  ), r = sn(
    a,
    t,
    /*$$scope*/
    t[11],
    null
  );
  return {
    c() {
      e = vl("a"), o && o.c(), l = rn(), r && r.c(), A(
        e,
        "href",
        /*link*/
        t[6]
      ), A(e, "rel", "noopener noreferrer"), A(
        e,
        "aria-disabled",
        /*disabled*/
        t[8]
      ), A(e, "class", n = /*size*/
      t[4] + " " + /*variant*/
      t[3] + " " + /*elem_classes*/
      t[1].join(" ") + " svelte-8huxfn"), A(
        e,
        "id",
        /*elem_id*/
        t[0]
      ), Oe(e, "hidden", !/*visible*/
      t[2]), Oe(
        e,
        "disabled",
        /*disabled*/
        t[8]
      ), U(
        e,
        "flex-grow",
        /*scale*/
        t[9]
      ), U(
        e,
        "pointer-events",
        /*disabled*/
        t[8] ? "none" : null
      ), U(
        e,
        "width",
        /*scale*/
        t[9] === 0 ? "fit-content" : null
      ), U(e, "min-width", typeof /*min_width*/
      t[10] == "number" ? `calc(min(${/*min_width*/
      t[10]}px, 100%))` : null);
    },
    m(f, s) {
      tl(f, e, s), o && o.m(e, null), on(e, l), r && r.m(e, null), i = !0;
    },
    p(f, s) {
      /*icon*/
      f[7] ? o ? o.p(f, s) : (o = yt(f), o.c(), o.m(e, l)) : o && (o.d(1), o = null), r && r.p && (!i || s & /*$$scope*/
      2048) && _n(
        r,
        a,
        f,
        /*$$scope*/
        f[11],
        i ? an(
          a,
          /*$$scope*/
          f[11],
          s,
          null
        ) : fn(
          /*$$scope*/
          f[11]
        ),
        null
      ), (!i || s & /*link*/
      64) && A(
        e,
        "href",
        /*link*/
        f[6]
      ), (!i || s & /*disabled*/
      256) && A(
        e,
        "aria-disabled",
        /*disabled*/
        f[8]
      ), (!i || s & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      f[4] + " " + /*variant*/
      f[3] + " " + /*elem_classes*/
      f[1].join(" ") + " svelte-8huxfn")) && A(e, "class", n), (!i || s & /*elem_id*/
      1) && A(
        e,
        "id",
        /*elem_id*/
        f[0]
      ), (!i || s & /*size, variant, elem_classes, visible*/
      30) && Oe(e, "hidden", !/*visible*/
      f[2]), (!i || s & /*size, variant, elem_classes, disabled*/
      282) && Oe(
        e,
        "disabled",
        /*disabled*/
        f[8]
      ), s & /*scale*/
      512 && U(
        e,
        "flex-grow",
        /*scale*/
        f[9]
      ), s & /*disabled*/
      256 && U(
        e,
        "pointer-events",
        /*disabled*/
        f[8] ? "none" : null
      ), s & /*scale*/
      512 && U(
        e,
        "width",
        /*scale*/
        f[9] === 0 ? "fit-content" : null
      ), s & /*min_width*/
      1024 && U(e, "min-width", typeof /*min_width*/
      f[10] == "number" ? `calc(min(${/*min_width*/
      f[10]}px, 100%))` : null);
    },
    i(f) {
      i || (dl(r, f), i = !0);
    },
    o(f) {
      ml(r, f), i = !1;
    },
    d(f) {
      f && ll(e), o && o.d(), r && r.d(f);
    }
  };
}
function kt(t) {
  let e, l, n;
  return {
    c() {
      e = vl("img"), A(e, "class", "button-icon svelte-8huxfn"), cl(e.src, l = /*icon*/
      t[7].url) || A(e, "src", l), A(e, "alt", n = `${/*value*/
      t[5]} icon`);
    },
    m(i, o) {
      tl(i, e, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !cl(e.src, l = /*icon*/
      i[7].url) && A(e, "src", l), o & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && A(e, "alt", n);
    },
    d(i) {
      i && ll(e);
    }
  };
}
function yt(t) {
  let e, l, n;
  return {
    c() {
      e = vl("img"), A(e, "class", "button-icon svelte-8huxfn"), cl(e.src, l = /*icon*/
      t[7].url) || A(e, "src", l), A(e, "alt", n = `${/*value*/
      t[5]} icon`);
    },
    m(i, o) {
      tl(i, e, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !cl(e.src, l = /*icon*/
      i[7].url) && A(e, "src", l), o & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && A(e, "alt", n);
    },
    d(i) {
      i && ll(e);
    }
  };
}
function $o(t) {
  let e, l, n, i;
  const o = [xo, Qo], a = [];
  function r(f, s) {
    return (
      /*link*/
      f[6] && /*link*/
      f[6].length > 0 ? 0 : 1
    );
  }
  return e = r(t), l = a[e] = o[e](t), {
    c() {
      l.c(), n = Uo();
    },
    m(f, s) {
      a[e].m(f, s), tl(f, n, s), i = !0;
    },
    p(f, [s]) {
      let _ = e;
      e = r(f), e === _ ? a[e].p(f, s) : (Wo(), ml(a[_], 1, 1, () => {
        a[_] = null;
      }), Ho(), l = a[e], l ? l.p(f, s) : (l = a[e] = o[e](f), l.c()), dl(l, 1), l.m(n.parentNode, n));
    },
    i(f) {
      i || (dl(l), i = !0);
    },
    o(f) {
      ml(l), i = !1;
    },
    d(f) {
      f && ll(n), a[e].d(f);
    }
  };
}
function es(t, e, l) {
  let { $$slots: n = {}, $$scope: i } = e, { elem_id: o = "" } = e, { elem_classes: a = [] } = e, { visible: r = !0 } = e, { variant: f = "secondary" } = e, { size: s = "lg" } = e, { value: _ = null } = e, { link: u = null } = e, { icon: c = null } = e, { disabled: d = !1 } = e, { scale: w = null } = e, { min_width: p = void 0 } = e;
  function v(k) {
    Xo.call(this, t, k);
  }
  return t.$$set = (k) => {
    "elem_id" in k && l(0, o = k.elem_id), "elem_classes" in k && l(1, a = k.elem_classes), "visible" in k && l(2, r = k.visible), "variant" in k && l(3, f = k.variant), "size" in k && l(4, s = k.size), "value" in k && l(5, _ = k.value), "link" in k && l(6, u = k.link), "icon" in k && l(7, c = k.icon), "disabled" in k && l(8, d = k.disabled), "scale" in k && l(9, w = k.scale), "min_width" in k && l(10, p = k.min_width), "$$scope" in k && l(11, i = k.$$scope);
  }, [
    o,
    a,
    r,
    f,
    s,
    _,
    u,
    c,
    d,
    w,
    p,
    i,
    n,
    v
  ];
}
class ls extends Go {
  constructor(e) {
    super(), Yo(this, e, es, $o, Ko, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
var qt = Object.prototype.hasOwnProperty;
function Ct(t, e, l) {
  for (l of t.keys())
    if (Qe(l, e))
      return l;
}
function Qe(t, e) {
  var l, n, i;
  if (t === e)
    return !0;
  if (t && e && (l = t.constructor) === e.constructor) {
    if (l === Date)
      return t.getTime() === e.getTime();
    if (l === RegExp)
      return t.toString() === e.toString();
    if (l === Array) {
      if ((n = t.length) === e.length)
        for (; n-- && Qe(t[n], e[n]); )
          ;
      return n === -1;
    }
    if (l === Set) {
      if (t.size !== e.size)
        return !1;
      for (n of t)
        if (i = n, i && typeof i == "object" && (i = Ct(e, i), !i) || !e.has(i))
          return !1;
      return !0;
    }
    if (l === Map) {
      if (t.size !== e.size)
        return !1;
      for (n of t)
        if (i = n[0], i && typeof i == "object" && (i = Ct(e, i), !i) || !Qe(n[1], e.get(i)))
          return !1;
      return !0;
    }
    if (l === ArrayBuffer)
      t = new Uint8Array(t), e = new Uint8Array(e);
    else if (l === DataView) {
      if ((n = t.byteLength) === e.byteLength)
        for (; n-- && t.getInt8(n) === e.getInt8(n); )
          ;
      return n === -1;
    }
    if (ArrayBuffer.isView(t)) {
      if ((n = t.byteLength) === e.byteLength)
        for (; n-- && t[n] === e[n]; )
          ;
      return n === -1;
    }
    if (!l || typeof t == "object") {
      n = 0;
      for (l in t)
        if (qt.call(t, l) && ++n && !qt.call(e, l) || !(l in e) || !Qe(t[l], e[l]))
          return !1;
      return Object.keys(e).length === n;
    }
  }
  return t !== t && e !== e;
}
const {
  SvelteComponent: ts,
  append: _l,
  attr: we,
  detach: Ol,
  element: hl,
  flush: Lt,
  init: ns,
  insert: Gl,
  listen: un,
  noop: Rl,
  safe_not_equal: is,
  set_data: os,
  space: zt,
  src_url_equal: St,
  text: ss
} = window.__gradio__svelte__internal, { createEventDispatcher: fs } = window.__gradio__svelte__internal;
function jt(t) {
  let e, l = (
    /*value*/
    t[1].caption + ""
  ), n;
  return {
    c() {
      e = hl("div"), n = ss(l), we(e, "class", "foot-label left-label svelte-1d4tgaw");
    },
    m(i, o) {
      Gl(i, e, o), _l(e, n);
    },
    p(i, o) {
      o & /*value*/
      2 && l !== (l = /*value*/
      i[1].caption + "") && os(n, l);
    },
    d(i) {
      i && Ol(e);
    }
  };
}
function Ft(t) {
  let e, l, n;
  return {
    c() {
      e = hl("button"), e.innerHTML = '<svg width="15" height="15" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="8" cy="8" r="8" fill="#FF6700"></circle><path d="M11.5797 10.6521C11.8406 10.913 11.8406 11.3188 11.5797 11.5797C11.4492 11.7101 11.2898 11.7681 11.1159 11.7681C10.942 11.7681 10.7826 11.7101 10.6521 11.5797L7.99997 8.92751L5.3478 11.5797C5.21736 11.7101 5.05794 11.7681 4.88403 11.7681C4.71012 11.7681 4.5507 11.7101 4.42026 11.5797C4.15939 11.3188 4.15939 10.913 4.42026 10.6521L7.07244 7.99997L4.42026 5.3478C4.15939 5.08693 4.15939 4.68113 4.42026 4.42026C4.68113 4.15939 5.08693 4.15939 5.3478 4.42026L7.99997 7.07244L10.6521 4.42026C10.913 4.15939 11.3188 4.15939 11.5797 4.42026C11.8406 4.68113 11.8406 5.08693 11.5797 5.3478L8.92751 7.99997L11.5797 10.6521Z" fill="#FFF4EA"></path></svg>', we(e, "class", "delete-button svelte-1d4tgaw");
    },
    m(i, o) {
      Gl(i, e, o), l || (n = un(
        e,
        "click",
        /*click_handler_1*/
        t[4]
      ), l = !0);
    },
    p: Rl,
    d(i) {
      i && Ol(e), l = !1, n();
    }
  };
}
function as(t) {
  let e, l, n, i, o, a, r, f, s = (
    /*value*/
    t[1].caption && jt(t)
  ), _ = (
    /*deletable*/
    t[0] && Ft(t)
  );
  return {
    c() {
      e = hl("div"), l = hl("img"), o = zt(), s && s.c(), a = zt(), _ && _.c(), we(l, "alt", n = /*value*/
      t[1].caption || ""), St(l.src, i = /*value*/
      t[1].image.url) || we(l, "src", i), we(l, "class", "thumbnail-img svelte-1d4tgaw"), we(l, "loading", "lazy"), we(e, "class", "thumbnail-image-box svelte-1d4tgaw");
    },
    m(u, c) {
      Gl(u, e, c), _l(e, l), _l(e, o), s && s.m(e, null), _l(e, a), _ && _.m(e, null), r || (f = un(
        l,
        "click",
        /*click_handler*/
        t[3]
      ), r = !0);
    },
    p(u, [c]) {
      c & /*value*/
      2 && n !== (n = /*value*/
      u[1].caption || "") && we(l, "alt", n), c & /*value*/
      2 && !St(l.src, i = /*value*/
      u[1].image.url) && we(l, "src", i), /*value*/
      u[1].caption ? s ? s.p(u, c) : (s = jt(u), s.c(), s.m(e, a)) : s && (s.d(1), s = null), /*deletable*/
      u[0] ? _ ? _.p(u, c) : (_ = Ft(u), _.c(), _.m(e, null)) : _ && (_.d(1), _ = null);
    },
    i: Rl,
    o: Rl,
    d(u) {
      u && Ol(e), s && s.d(), _ && _.d(), r = !1, f();
    }
  };
}
function rs(t, e, l) {
  const n = fs();
  let { deletable: i } = e, { value: o } = e;
  const a = () => n("click"), r = () => {
    n("delete_image", o);
  };
  return t.$$set = (f) => {
    "deletable" in f && l(0, i = f.deletable), "value" in f && l(1, o = f.value);
  }, [i, o, n, a, r];
}
class _s extends ts {
  constructor(e) {
    super(), ns(this, e, rs, as, is, { deletable: 0, value: 1 });
  }
  get deletable() {
    return this.$$.ctx[0];
  }
  set deletable(e) {
    this.$$set({ deletable: e }), Lt();
  }
  get value() {
    return this.$$.ctx[1];
  }
  set value(e) {
    this.$$set({ value: e }), Lt();
  }
}
const Bl = [
  {
    key: "xs",
    width: 0
  },
  {
    key: "sm",
    width: 576
  },
  {
    key: "md",
    width: 768
  },
  {
    key: "lg",
    width: 992
  },
  {
    key: "xl",
    width: 1200
  },
  {
    key: "xxl",
    width: 1600
  }
];
async function us(t) {
  if ("clipboard" in navigator)
    await navigator.clipboard.writeText(t);
  else {
    const e = document.createElement("textarea");
    e.value = t, e.style.position = "absolute", e.style.left = "-999999px", document.body.prepend(e), e.select();
    try {
      document.execCommand("copy");
    } catch (l) {
      return Promise.reject(l);
    } finally {
      e.remove();
    }
  }
}
async function cs(t) {
  return t ? `<div style="display: flex; flex-wrap: wrap; gap: 16px">${(await Promise.all(
    t.map((l) => !l.image || !l.image.url ? "" : l.image.url)
  )).map((l) => `<img src="${l}" style="height: 400px" />`).join("")}</div>` : "";
}
const {
  SvelteComponent: ds,
  add_iframe_resize_listener: ms,
  add_render_callback: cn,
  append: W,
  assign: hs,
  attr: E,
  binding_callbacks: Mt,
  bubble: bs,
  check_outros: xe,
  create_component: Ie,
  destroy_component: Be,
  destroy_each: dn,
  detach: de,
  element: Q,
  empty: gs,
  ensure_array_like: bl,
  get_spread_object: ws,
  get_spread_update: vs,
  group_outros: $e,
  init: ps,
  insert: me,
  listen: gl,
  mount_component: De,
  noop: ks,
  run_all: ys,
  safe_not_equal: qs,
  set_data: mn,
  set_style: qe,
  space: Le,
  src_url_equal: wl,
  text: hn,
  toggle_class: $,
  transition_in: N,
  transition_out: T
} = window.__gradio__svelte__internal, { createEventDispatcher: Cs, tick: Ls } = window.__gradio__svelte__internal;
function Et(t, e, l) {
  const n = t.slice();
  return n[51] = e[l], n[53] = l, n;
}
function At(t, e, l) {
  const n = t.slice();
  return n[51] = e[l], n[54] = e, n[53] = l, n;
}
function It(t) {
  let e, l;
  return e = new Yn({
    props: {
      show_label: (
        /*show_label*/
        t[2]
      ),
      Icon: Ht,
      label: (
        /*label*/
        t[4] || "Gallery"
      )
    }
  }), {
    c() {
      Ie(e.$$.fragment);
    },
    m(n, i) {
      De(e, n, i), l = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*show_label*/
      4 && (o.show_label = /*show_label*/
      n[2]), i[0] & /*label*/
      16 && (o.label = /*label*/
      n[4] || "Gallery"), e.$set(o);
    },
    i(n) {
      l || (N(e.$$.fragment, n), l = !0);
    },
    o(n) {
      T(e.$$.fragment, n), l = !1;
    },
    d(n) {
      Be(e, n);
    }
  };
}
function zs(t) {
  let e, l, n, i, o, a, r, f, s, _, u, c = (
    /*selected_image*/
    t[19] && /*allow_preview*/
    t[8] && Bt(t)
  ), d = (
    /*show_share_button*/
    t[9] && Nt(t)
  ), w = bl(
    /*resolved_value*/
    t[14]
  ), p = [];
  for (let m = 0; m < w.length; m += 1)
    p[m] = Zt(Et(t, w, m));
  const v = (m) => T(p[m], 1, 1, () => {
    p[m] = null;
  }), k = [Fs, js], h = [];
  function b(m, L) {
    return (
      /*pending*/
      m[5] ? 0 : 1
    );
  }
  return f = b(t), s = h[f] = k[f](t), {
    c() {
      c && c.c(), e = Le(), l = Q("div"), n = Q("div"), d && d.c(), i = Le(), o = Q("div");
      for (let m = 0; m < p.length; m += 1)
        p[m].c();
      a = Le(), r = Q("p"), s.c(), E(n, "class", "grid-container svelte-1q36pmh"), qe(
        n,
        "--object-fit",
        /*object_fit*/
        t[1]
      ), qe(
        n,
        "min-height",
        /*height*/
        t[7] + "px"
      ), $(
        n,
        "pt-6",
        /*show_label*/
        t[2]
      ), E(r, "class", "loading-line svelte-1q36pmh"), $(r, "visible", !/*selected_image*/
      (t[19] && /*allow_preview*/
      t[8]) && /*has_more*/
      t[3]), E(l, "class", "grid-wrap svelte-1q36pmh"), qe(
        l,
        "height",
        /*height*/
        t[7] + "px"
      ), cn(() => (
        /*div2_elementresize_handler*/
        t[45].call(l)
      )), $(l, "fixed-height", !/*height*/
      t[7] || /*height*/
      t[7] === "auto");
    },
    m(m, L) {
      c && c.m(m, L), me(m, e, L), me(m, l, L), W(l, n), d && d.m(n, null), W(n, i), W(n, o);
      for (let q = 0; q < p.length; q += 1)
        p[q] && p[q].m(o, null);
      W(l, a), W(l, r), h[f].m(r, null), _ = ms(
        l,
        /*div2_elementresize_handler*/
        t[45].bind(l)
      ), u = !0;
    },
    p(m, L) {
      if (/*selected_image*/
      m[19] && /*allow_preview*/
      m[8] ? c ? c.p(m, L) : (c = Bt(m), c.c(), c.m(e.parentNode, e)) : c && (c.d(1), c = null), /*show_share_button*/
      m[9] ? d ? (d.p(m, L), L[0] & /*show_share_button*/
      512 && N(d, 1)) : (d = Nt(m), d.c(), N(d, 1), d.m(n, i)) : d && ($e(), T(d, 1, 1, () => {
        d = null;
      }), xe()), L[0] & /*resolved_value, selected_index, deletable, handleDeleteImage*/
      4211713) {
        w = bl(
          /*resolved_value*/
          m[14]
        );
        let F;
        for (F = 0; F < w.length; F += 1) {
          const Z = Et(m, w, F);
          p[F] ? (p[F].p(Z, L), N(p[F], 1)) : (p[F] = Zt(Z), p[F].c(), N(p[F], 1), p[F].m(o, null));
        }
        for ($e(), F = w.length; F < p.length; F += 1)
          v(F);
        xe();
      }
      (!u || L[0] & /*object_fit*/
      2) && qe(
        n,
        "--object-fit",
        /*object_fit*/
        m[1]
      ), (!u || L[0] & /*height*/
      128) && qe(
        n,
        "min-height",
        /*height*/
        m[7] + "px"
      ), (!u || L[0] & /*show_label*/
      4) && $(
        n,
        "pt-6",
        /*show_label*/
        m[2]
      );
      let q = f;
      f = b(m), f === q ? h[f].p(m, L) : ($e(), T(h[q], 1, 1, () => {
        h[q] = null;
      }), xe(), s = h[f], s ? s.p(m, L) : (s = h[f] = k[f](m), s.c()), N(s, 1), s.m(r, null)), (!u || L[0] & /*selected_image, allow_preview, has_more*/
      524552) && $(r, "visible", !/*selected_image*/
      (m[19] && /*allow_preview*/
      m[8]) && /*has_more*/
      m[3]), (!u || L[0] & /*height*/
      128) && qe(
        l,
        "height",
        /*height*/
        m[7] + "px"
      ), (!u || L[0] & /*height*/
      128) && $(l, "fixed-height", !/*height*/
      m[7] || /*height*/
      m[7] === "auto");
    },
    i(m) {
      if (!u) {
        N(d);
        for (let L = 0; L < w.length; L += 1)
          N(p[L]);
        N(s), u = !0;
      }
    },
    o(m) {
      T(d), p = p.filter(Boolean);
      for (let L = 0; L < p.length; L += 1)
        T(p[L]);
      T(s), u = !1;
    },
    d(m) {
      m && (de(e), de(l)), c && c.d(m), d && d.d(), dn(p, m), h[f].d(), _();
    }
  };
}
function Ss(t) {
  let e, l;
  return e = new Li({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [Es] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      Ie(e.$$.fragment);
    },
    m(n, i) {
      De(e, n, i), l = !0;
    },
    p(n, i) {
      const o = {};
      i[1] & /*$$scope*/
      16777216 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      l || (N(e.$$.fragment, n), l = !0);
    },
    o(n) {
      T(e.$$.fragment, n), l = !1;
    },
    d(n) {
      Be(e, n);
    }
  };
}
function Bt(t) {
  var p;
  let e, l, n, i, o, a, r, f, s, _, u, c = (
    /*selected_image*/
    ((p = t[19]) == null ? void 0 : p.caption) && Dt(t)
  ), d = bl(
    /*resolved_value*/
    t[14]
  ), w = [];
  for (let v = 0; v < d.length; v += 1)
    w[v] = Vt(At(t, d, v));
  return {
    c() {
      e = Q("button"), l = Q("button"), n = Q("img"), r = Le(), c && c.c(), f = Le(), s = Q("div");
      for (let v = 0; v < w.length; v += 1)
        w[v].c();
      E(n, "data-testid", "detailed-image"), wl(n.src, i = /*selected_image*/
      t[19].image.url) || E(n, "src", i), E(n, "alt", o = /*selected_image*/
      t[19].caption || ""), E(n, "title", a = /*selected_image*/
      t[19].caption || null), E(n, "loading", "lazy"), E(n, "class", "svelte-1q36pmh"), $(n, "with-caption", !!/*selected_image*/
      t[19].caption), E(l, "class", "image-button svelte-1q36pmh"), qe(l, "height", "calc(100% - " + /*selected_image*/
      (t[19].caption ? "80px" : "60px") + ")"), E(l, "aria-label", "detailed view of selected image"), E(s, "class", "thumbnails scroll-hide svelte-1q36pmh"), E(s, "data-testid", "container_el"), E(e, "class", "preview svelte-1q36pmh");
    },
    m(v, k) {
      me(v, e, k), W(e, l), W(l, n), W(e, r), c && c.m(e, null), W(e, f), W(e, s);
      for (let h = 0; h < w.length; h += 1)
        w[h] && w[h].m(s, null);
      t[39](s), _ || (u = [
        gl(
          l,
          "click",
          /*click_handler*/
          t[36]
        ),
        gl(
          e,
          "keydown",
          /*on_keydown*/
          t[23]
        )
      ], _ = !0);
    },
    p(v, k) {
      var h;
      if (k[0] & /*selected_image*/
      524288 && !wl(n.src, i = /*selected_image*/
      v[19].image.url) && E(n, "src", i), k[0] & /*selected_image*/
      524288 && o !== (o = /*selected_image*/
      v[19].caption || "") && E(n, "alt", o), k[0] & /*selected_image*/
      524288 && a !== (a = /*selected_image*/
      v[19].caption || null) && E(n, "title", a), k[0] & /*selected_image*/
      524288 && $(n, "with-caption", !!/*selected_image*/
      v[19].caption), k[0] & /*selected_image*/
      524288 && qe(l, "height", "calc(100% - " + /*selected_image*/
      (v[19].caption ? "80px" : "60px") + ")"), /*selected_image*/
      (h = v[19]) != null && h.caption ? c ? c.p(v, k) : (c = Dt(v), c.c(), c.m(e, f)) : c && (c.d(1), c = null), k[0] & /*resolved_value, el, selected_index*/
      147457) {
        d = bl(
          /*resolved_value*/
          v[14]
        );
        let b;
        for (b = 0; b < d.length; b += 1) {
          const m = At(v, d, b);
          w[b] ? w[b].p(m, k) : (w[b] = Vt(m), w[b].c(), w[b].m(s, null));
        }
        for (; b < w.length; b += 1)
          w[b].d(1);
        w.length = d.length;
      }
    },
    d(v) {
      v && de(e), c && c.d(), dn(w, v), t[39](null), _ = !1, ys(u);
    }
  };
}
function Dt(t) {
  let e, l = (
    /*selected_image*/
    t[19].caption + ""
  ), n;
  return {
    c() {
      e = Q("caption"), n = hn(l), E(e, "class", "caption svelte-1q36pmh");
    },
    m(i, o) {
      me(i, e, o), W(e, n);
    },
    p(i, o) {
      o[0] & /*selected_image*/
      524288 && l !== (l = /*selected_image*/
      i[19].caption + "") && mn(n, l);
    },
    d(i) {
      i && de(e);
    }
  };
}
function Vt(t) {
  let e, l, n, i, o, a, r = (
    /*i*/
    t[53]
  ), f, s;
  const _ = () => (
    /*button_binding*/
    t[37](e, r)
  ), u = () => (
    /*button_binding*/
    t[37](null, r)
  );
  function c() {
    return (
      /*click_handler_1*/
      t[38](
        /*i*/
        t[53]
      )
    );
  }
  return {
    c() {
      e = Q("button"), l = Q("img"), o = Le(), wl(l.src, n = /*entry*/
      t[51].image.url) || E(l, "src", n), E(l, "title", i = /*entry*/
      t[51].caption || null), E(l, "data-testid", "thumbnail " + /*i*/
      (t[53] + 1)), E(l, "alt", ""), E(l, "loading", "lazy"), E(l, "class", "svelte-1q36pmh"), E(e, "class", "thumbnail-item thumbnail-small svelte-1q36pmh"), E(e, "aria-label", a = "Thumbnail " + /*i*/
      (t[53] + 1) + " of " + /*resolved_value*/
      t[14].length), $(
        e,
        "selected",
        /*selected_index*/
        t[0] === /*i*/
        t[53]
      );
    },
    m(d, w) {
      me(d, e, w), W(e, l), W(e, o), _(), f || (s = gl(e, "click", c), f = !0);
    },
    p(d, w) {
      t = d, w[0] & /*resolved_value*/
      16384 && !wl(l.src, n = /*entry*/
      t[51].image.url) && E(l, "src", n), w[0] & /*resolved_value*/
      16384 && i !== (i = /*entry*/
      t[51].caption || null) && E(l, "title", i), w[0] & /*resolved_value*/
      16384 && a !== (a = "Thumbnail " + /*i*/
      (t[53] + 1) + " of " + /*resolved_value*/
      t[14].length) && E(e, "aria-label", a), r !== /*i*/
      t[53] && (u(), r = /*i*/
      t[53], _()), w[0] & /*selected_index*/
      1 && $(
        e,
        "selected",
        /*selected_index*/
        t[0] === /*i*/
        t[53]
      );
    },
    d(d) {
      d && de(e), u(), f = !1, s();
    }
  };
}
function Nt(t) {
  let e, l, n;
  return l = new so({
    props: {
      i18n: (
        /*i18n*/
        t[11]
      ),
      value: (
        /*resolved_value*/
        t[14]
      ),
      formatter: cs
    }
  }), l.$on(
    "share",
    /*share_handler*/
    t[40]
  ), l.$on(
    "error",
    /*error_handler*/
    t[41]
  ), {
    c() {
      e = Q("div"), Ie(l.$$.fragment), E(e, "class", "icon-button svelte-1q36pmh");
    },
    m(i, o) {
      me(i, e, o), De(l, e, null), n = !0;
    },
    p(i, o) {
      const a = {};
      o[0] & /*i18n*/
      2048 && (a.i18n = /*i18n*/
      i[11]), o[0] & /*resolved_value*/
      16384 && (a.value = /*resolved_value*/
      i[14]), l.$set(a);
    },
    i(i) {
      n || (N(l.$$.fragment, i), n = !0);
    },
    o(i) {
      T(l.$$.fragment, i), n = !1;
    },
    d(i) {
      i && de(e), Be(l);
    }
  };
}
function Zt(t) {
  let e, l, n, i, o;
  function a() {
    return (
      /*click_handler_2*/
      t[42](
        /*i*/
        t[53]
      )
    );
  }
  return l = new _s({
    props: {
      deletable: (
        /*deletable*/
        t[10]
      ),
      value: (
        /*entry*/
        t[51]
      )
    }
  }), l.$on("click", a), l.$on(
    "delete_image",
    /*delete_image_handler*/
    t[43]
  ), {
    c() {
      e = Q("div"), Ie(l.$$.fragment), n = Le(), E(e, "class", "thumbnail-item thumbnail-lg svelte-1q36pmh"), E(e, "aria-label", i = "Thumbnail " + /*i*/
      (t[53] + 1) + " of " + /*resolved_value*/
      t[14].length), $(
        e,
        "selected",
        /*selected_index*/
        t[0] === /*i*/
        t[53]
      );
    },
    m(r, f) {
      me(r, e, f), De(l, e, null), W(e, n), o = !0;
    },
    p(r, f) {
      t = r;
      const s = {};
      f[0] & /*deletable*/
      1024 && (s.deletable = /*deletable*/
      t[10]), f[0] & /*resolved_value*/
      16384 && (s.value = /*entry*/
      t[51]), l.$set(s), (!o || f[0] & /*resolved_value*/
      16384 && i !== (i = "Thumbnail " + /*i*/
      (t[53] + 1) + " of " + /*resolved_value*/
      t[14].length)) && E(e, "aria-label", i), (!o || f[0] & /*selected_index*/
      1) && $(
        e,
        "selected",
        /*selected_index*/
        t[0] === /*i*/
        t[53]
      );
    },
    i(r) {
      o || (N(l.$$.fragment, r), o = !0);
    },
    o(r) {
      T(l.$$.fragment, r), o = !1;
    },
    d(r) {
      r && de(e), Be(l);
    }
  };
}
function js(t) {
  let e, l;
  const n = [
    /*load_more_button_props*/
    t[12]
  ];
  let i = {
    $$slots: { default: [Ms] },
    $$scope: { ctx: t }
  };
  for (let o = 0; o < n.length; o += 1)
    i = hs(i, n[o]);
  return e = new ls({ props: i }), e.$on(
    "click",
    /*click_handler_3*/
    t[44]
  ), {
    c() {
      Ie(e.$$.fragment);
    },
    m(o, a) {
      De(e, o, a), l = !0;
    },
    p(o, a) {
      const r = a[0] & /*load_more_button_props*/
      4096 ? vs(n, [ws(
        /*load_more_button_props*/
        o[12]
      )]) : {};
      a[0] & /*i18n, load_more_button_props*/
      6144 | a[1] & /*$$scope*/
      16777216 && (r.$$scope = { dirty: a, ctx: o }), e.$set(r);
    },
    i(o) {
      l || (N(e.$$.fragment, o), l = !0);
    },
    o(o) {
      T(e.$$.fragment, o), l = !1;
    },
    d(o) {
      Be(e, o);
    }
  };
}
function Fs(t) {
  let e, l;
  return e = new Jt({ props: { margin: !1 } }), {
    c() {
      Ie(e.$$.fragment);
    },
    m(n, i) {
      De(e, n, i), l = !0;
    },
    p: ks,
    i(n) {
      l || (N(e.$$.fragment, n), l = !0);
    },
    o(n) {
      T(e.$$.fragment, n), l = !1;
    },
    d(n) {
      Be(e, n);
    }
  };
}
function Ms(t) {
  let e = (
    /*i18n*/
    t[11](
      /*load_more_button_props*/
      t[12].value || /*load_more_button_props*/
      t[12].label || "Load More"
    ) + ""
  ), l;
  return {
    c() {
      l = hn(e);
    },
    m(n, i) {
      me(n, l, i);
    },
    p(n, i) {
      i[0] & /*i18n, load_more_button_props*/
      6144 && e !== (e = /*i18n*/
      n[11](
        /*load_more_button_props*/
        n[12].value || /*load_more_button_props*/
        n[12].label || "Load More"
      ) + "") && mn(l, e);
    },
    d(n) {
      n && de(l);
    }
  };
}
function Es(t) {
  let e, l;
  return e = new Ht({}), {
    c() {
      Ie(e.$$.fragment);
    },
    m(n, i) {
      De(e, n, i), l = !0;
    },
    i(n) {
      l || (N(e.$$.fragment, n), l = !0);
    },
    o(n) {
      T(e.$$.fragment, n), l = !1;
    },
    d(n) {
      Be(e, n);
    }
  };
}
function As(t) {
  let e, l, n, i, o, a, r;
  cn(
    /*onwindowresize*/
    t[35]
  );
  let f = (
    /*show_label*/
    t[2] && It(t)
  );
  const s = [Ss, zs], _ = [];
  function u(c, d) {
    return !/*value*/
    c[6] || !/*resolved_value*/
    c[14] || /*resolved_value*/
    c[14].length === 0 ? 0 : 1;
  }
  return l = u(t), n = _[l] = s[l](t), {
    c() {
      f && f.c(), e = Le(), n.c(), i = gs();
    },
    m(c, d) {
      f && f.m(c, d), me(c, e, d), _[l].m(c, d), me(c, i, d), o = !0, a || (r = gl(
        window,
        "resize",
        /*onwindowresize*/
        t[35]
      ), a = !0);
    },
    p(c, d) {
      /*show_label*/
      c[2] ? f ? (f.p(c, d), d[0] & /*show_label*/
      4 && N(f, 1)) : (f = It(c), f.c(), N(f, 1), f.m(e.parentNode, e)) : f && ($e(), T(f, 1, 1, () => {
        f = null;
      }), xe());
      let w = l;
      l = u(c), l === w ? _[l].p(c, d) : ($e(), T(_[w], 1, 1, () => {
        _[w] = null;
      }), xe(), n = _[l], n ? n.p(c, d) : (n = _[l] = s[l](c), n.c()), N(n, 1), n.m(i.parentNode, i));
    },
    i(c) {
      o || (N(f), N(n), o = !0);
    },
    o(c) {
      T(f), T(n), o = !1;
    },
    d(c) {
      c && (de(e), de(i)), f && f.d(c), _[l].d(c), a = !1, r();
    }
  };
}
function Is(t, e, l) {
  let n, i, o;
  var a = this && this.__awaiter || function(g, O, X, te) {
    function Ye(Me) {
      return Me instanceof X ? Me : new X(function(Je) {
        Je(Me);
      });
    }
    return new (X || (X = Promise))(function(Me, Je) {
      function nl(Ee) {
        try {
          Cl(te.next(Ee));
        } catch (Ll) {
          Je(Ll);
        }
      }
      function bn(Ee) {
        try {
          Cl(te.throw(Ee));
        } catch (Ll) {
          Je(Ll);
        }
      }
      function Cl(Ee) {
        Ee.done ? Me(Ee.value) : Ye(Ee.value).then(nl, bn);
      }
      Cl((te = te.apply(g, O || [])).next());
    });
  }, r, f, s;
  let { object_fit: _ = "cover" } = e, { show_label: u = !0 } = e, { has_more: c = !1 } = e, { label: d } = e, { pending: w } = e, { value: p = null } = e, { columns: v = [2] } = e, { height: k = "auto" } = e, { preview: h = !1 } = e, { proxy_url: b } = e, { allow_preview: m = !1 } = e, { show_share_button: L = !1 } = e, { deletable: q } = e, { show_download_button: F = !1 } = e, { i18n: Z } = e, { selected_index: j = null } = e, { load_more_button_props: D = {} } = e, P = [], G = 0, ze = 0, Y = 0;
  const J = Cs();
  let R = !0, B = null, Se = p;
  j == null && h && (p != null && p.length) && (j = 0);
  let ve = j;
  function je(g) {
    const O = g.target, X = g.clientX, Ye = O.offsetWidth / 2;
    X < Ye ? l(0, j = n) : l(0, j = i);
  }
  function he(g) {
    J("delete_image", g.detail.image.orig_name);
  }
  function y(g) {
    switch (g.code) {
      case "Escape":
        g.preventDefault();
        break;
      case "ArrowLeft":
        g.preventDefault(), l(0, j = n);
        break;
      case "ArrowRight":
        g.preventDefault(), l(0, j = i);
        break;
    }
  }
  let pe = [], ae;
  function C(g) {
    return a(this, void 0, void 0, function* () {
      var O;
      if (typeof g != "number" || (yield Ls(), pe[g] === void 0))
        return;
      (O = pe[g]) === null || O === void 0 || O.focus();
      const { left: X, width: te } = ae.getBoundingClientRect(), { left: Ye, width: Me } = pe[g].getBoundingClientRect(), nl = Ye - X + Me / 2 - te / 2 + ae.scrollLeft;
      ae && typeof ae.scrollTo == "function" && ae.scrollTo({
        left: nl < 0 ? 0 : nl,
        behavior: "smooth"
      });
    });
  }
  function pl() {
    l(16, ze = window.innerHeight), l(13, Y = window.innerWidth);
  }
  const Ve = (g) => je(g);
  function Ne(g, O) {
    Mt[g ? "unshift" : "push"](() => {
      pe[O] = g, l(17, pe);
    });
  }
  const kl = (g) => l(0, j = g);
  function Fe(g) {
    Mt[g ? "unshift" : "push"](() => {
      ae = g, l(18, ae);
    });
  }
  const Ze = (g) => {
    us(g.detail.description);
  };
  function yl(g) {
    bs.call(this, t, g);
  }
  const ql = (g) => l(0, j = g), Ue = (g) => he(g), be = () => {
    J("load_more");
  };
  function We() {
    G = this.clientHeight, l(15, G);
  }
  return t.$$set = (g) => {
    "object_fit" in g && l(1, _ = g.object_fit), "show_label" in g && l(2, u = g.show_label), "has_more" in g && l(3, c = g.has_more), "label" in g && l(4, d = g.label), "pending" in g && l(5, w = g.pending), "value" in g && l(6, p = g.value), "columns" in g && l(24, v = g.columns), "height" in g && l(7, k = g.height), "preview" in g && l(25, h = g.preview), "proxy_url" in g && l(26, b = g.proxy_url), "allow_preview" in g && l(8, m = g.allow_preview), "show_share_button" in g && l(9, L = g.show_share_button), "deletable" in g && l(10, q = g.deletable), "show_download_button" in g && l(27, F = g.show_download_button), "i18n" in g && l(11, Z = g.i18n), "selected_index" in g && l(0, j = g.selected_index), "load_more_button_props" in g && l(12, D = g.load_more_button_props);
  }, t.$$.update = () => {
    if (t.$$.dirty[0] & /*columns*/
    16777216)
      if (typeof v == "object" && v !== null)
        if (Array.isArray(v)) {
          const g = v.length;
          l(31, P = Bl.map((O, X) => {
            var te;
            return [
              O.width,
              (te = v[X]) !== null && te !== void 0 ? te : v[g - 1]
            ];
          }));
        } else {
          let g = 0;
          l(31, P = Bl.map((O) => {
            const X = v[O.key];
            return g = X ?? g, [O.width, g];
          }));
        }
      else
        l(31, P = Bl.map((g) => [g.width, v]));
    if (t.$$.dirty[0] & /*window_width*/
    8192 | t.$$.dirty[1] & /*breakpointColumns*/
    1) {
      for (const [g, O] of [...P].reverse())
        if (Y >= g)
          break;
    }
    t.$$.dirty[0] & /*value*/
    64 | t.$$.dirty[1] & /*was_reset*/
    2 && l(32, R = p == null || p.length === 0 ? !0 : R), t.$$.dirty[0] & /*value*/
    64 && l(14, B = p == null ? null : p.map((g) => g)), t.$$.dirty[0] & /*value, preview, selected_index*/
    33554497 | t.$$.dirty[1] & /*prev_value, was_reset*/
    6 && (Qe(Se, p) || (R ? (l(0, j = h && (p != null && p.length) ? j ?? 0 : null), l(32, R = !1)) : l(0, j = j != null && p != null && j < p.length ? j : null), J("change"), l(33, Se = p))), t.$$.dirty[0] & /*selected_index, resolved_value, _a, _b*/
    805322753 && (n = ((j ?? 0) + (l(28, r = B == null ? void 0 : B.length) !== null && r !== void 0 ? r : 0) - 1) % (l(29, f = B == null ? void 0 : B.length) !== null && f !== void 0 ? f : 0)), t.$$.dirty[0] & /*selected_index, resolved_value, _c*/
    1073758209 && (i = ((j ?? 0) + 1) % (l(30, s = B == null ? void 0 : B.length) !== null && s !== void 0 ? s : 0)), t.$$.dirty[0] & /*selected_index, resolved_value*/
    16385 | t.$$.dirty[1] & /*old_selected_index*/
    8 && j !== ve && (l(34, ve = j), j !== null && J("select", {
      index: j,
      value: B == null ? void 0 : B[j]
    })), t.$$.dirty[0] & /*allow_preview, selected_index*/
    257 && m && C(j), t.$$.dirty[0] & /*selected_index, resolved_value*/
    16385 && l(19, o = j != null && B != null ? B[j] : null);
  }, [
    j,
    _,
    u,
    c,
    d,
    w,
    p,
    k,
    m,
    L,
    q,
    Z,
    D,
    Y,
    B,
    G,
    ze,
    pe,
    ae,
    o,
    J,
    je,
    he,
    y,
    v,
    h,
    b,
    F,
    r,
    f,
    s,
    P,
    R,
    Se,
    ve,
    pl,
    Ve,
    Ne,
    kl,
    Fe,
    Ze,
    yl,
    ql,
    Ue,
    be,
    We
  ];
}
class Bs extends ds {
  constructor(e) {
    super(), ps(
      this,
      e,
      Is,
      As,
      qs,
      {
        object_fit: 1,
        show_label: 2,
        has_more: 3,
        label: 4,
        pending: 5,
        value: 6,
        columns: 24,
        height: 7,
        preview: 25,
        proxy_url: 26,
        allow_preview: 8,
        show_share_button: 9,
        deletable: 10,
        show_download_button: 27,
        i18n: 11,
        selected_index: 0,
        load_more_button_props: 12
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Ds,
  add_flush_callback: Vs,
  assign: Ns,
  bind: Zs,
  binding_callbacks: Ts,
  check_outros: Ps,
  create_component: Xl,
  destroy_component: Hl,
  detach: Rs,
  get_spread_object: Os,
  get_spread_update: Gs,
  group_outros: Xs,
  init: Hs,
  insert: Us,
  mount_component: Ul,
  safe_not_equal: Ws,
  space: Ys,
  transition_in: Ge,
  transition_out: el
} = window.__gradio__svelte__internal, { createEventDispatcher: Js } = window.__gradio__svelte__internal;
function Tt(t) {
  let e, l;
  const n = [
    {
      autoscroll: (
        /*gradio*/
        t[23].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      t[23].i18n
    ) },
    /*loading_status*/
    t[1],
    {
      show_progress: (
        /*loading_status*/
        t[1].show_progress === "hidden" ? "hidden" : (
          /*has_more*/
          t[3] ? "minimal" : (
            /*loading_status*/
            t[1].show_progress
          )
        )
      )
    }
  ];
  let i = {};
  for (let o = 0; o < n.length; o += 1)
    i = Ns(i, n[o]);
  return e = new Oo({ props: i }), {
    c() {
      Xl(e.$$.fragment);
    },
    m(o, a) {
      Ul(e, o, a), l = !0;
    },
    p(o, a) {
      const r = a[0] & /*gradio, loading_status, has_more*/
      8388618 ? Gs(n, [
        a[0] & /*gradio*/
        8388608 && {
          autoscroll: (
            /*gradio*/
            o[23].autoscroll
          )
        },
        a[0] & /*gradio*/
        8388608 && { i18n: (
          /*gradio*/
          o[23].i18n
        ) },
        a[0] & /*loading_status*/
        2 && Os(
          /*loading_status*/
          o[1]
        ),
        a[0] & /*loading_status, has_more*/
        10 && {
          show_progress: (
            /*loading_status*/
            o[1].show_progress === "hidden" ? "hidden" : (
              /*has_more*/
              o[3] ? "minimal" : (
                /*loading_status*/
                o[1].show_progress
              )
            )
          )
        }
      ]) : {};
      e.$set(r);
    },
    i(o) {
      l || (Ge(e.$$.fragment, o), l = !0);
    },
    o(o) {
      el(e.$$.fragment, o), l = !1;
    },
    d(o) {
      Hl(e, o);
    }
  };
}
function Ks(t) {
  var f;
  let e, l, n, i, o = (
    /*loading_status*/
    t[1] && Tt(t)
  );
  function a(s) {
    t[26](s);
  }
  let r = {
    pending: (
      /*loading_status*/
      ((f = t[1]) == null ? void 0 : f.status) === "pending"
    ),
    deletable: (
      /*deletable*/
      t[9]
    ),
    label: (
      /*label*/
      t[4]
    ),
    value: (
      /*value*/
      t[8]
    ),
    root: (
      /*root*/
      t[21]
    ),
    proxy_url: (
      /*proxy_url*/
      t[22]
    ),
    show_label: (
      /*show_label*/
      t[2]
    ),
    object_fit: (
      /*object_fit*/
      t[19]
    ),
    load_more_button_props: (
      /*_load_more_button_props*/
      t[24]
    ),
    has_more: (
      /*has_more*/
      t[3]
    ),
    columns: (
      /*columns*/
      t[13]
    ),
    height: (
      /*height*/
      t[15]
    ),
    preview: (
      /*preview*/
      t[16]
    ),
    gap: (
      /*gap*/
      t[14]
    ),
    allow_preview: (
      /*allow_preview*/
      t[17]
    ),
    show_share_button: (
      /*show_share_button*/
      t[18]
    ),
    show_download_button: (
      /*show_download_button*/
      t[20]
    ),
    i18n: (
      /*gradio*/
      t[23].i18n
    )
  };
  return (
    /*selected_index*/
    t[0] !== void 0 && (r.selected_index = /*selected_index*/
    t[0]), l = new Bs({ props: r }), Ts.push(() => Zs(l, "selected_index", a)), l.$on(
      "click",
      /*click_handler*/
      t[27]
    ), l.$on(
      "change",
      /*change_handler*/
      t[28]
    ), l.$on(
      "select",
      /*select_handler*/
      t[29]
    ), l.$on(
      "share",
      /*share_handler*/
      t[30]
    ), l.$on(
      "error",
      /*error_handler*/
      t[31]
    ), l.$on(
      "delete_image",
      /*delete_image_handler*/
      t[32]
    ), l.$on(
      "load_more",
      /*load_more_handler*/
      t[33]
    ), {
      c() {
        o && o.c(), e = Ys(), Xl(l.$$.fragment);
      },
      m(s, _) {
        o && o.m(s, _), Us(s, e, _), Ul(l, s, _), i = !0;
      },
      p(s, _) {
        var c;
        /*loading_status*/
        s[1] ? o ? (o.p(s, _), _[0] & /*loading_status*/
        2 && Ge(o, 1)) : (o = Tt(s), o.c(), Ge(o, 1), o.m(e.parentNode, e)) : o && (Xs(), el(o, 1, 1, () => {
          o = null;
        }), Ps());
        const u = {};
        _[0] & /*loading_status*/
        2 && (u.pending = /*loading_status*/
        ((c = s[1]) == null ? void 0 : c.status) === "pending"), _[0] & /*deletable*/
        512 && (u.deletable = /*deletable*/
        s[9]), _[0] & /*label*/
        16 && (u.label = /*label*/
        s[4]), _[0] & /*value*/
        256 && (u.value = /*value*/
        s[8]), _[0] & /*root*/
        2097152 && (u.root = /*root*/
        s[21]), _[0] & /*proxy_url*/
        4194304 && (u.proxy_url = /*proxy_url*/
        s[22]), _[0] & /*show_label*/
        4 && (u.show_label = /*show_label*/
        s[2]), _[0] & /*object_fit*/
        524288 && (u.object_fit = /*object_fit*/
        s[19]), _[0] & /*_load_more_button_props*/
        16777216 && (u.load_more_button_props = /*_load_more_button_props*/
        s[24]), _[0] & /*has_more*/
        8 && (u.has_more = /*has_more*/
        s[3]), _[0] & /*columns*/
        8192 && (u.columns = /*columns*/
        s[13]), _[0] & /*height*/
        32768 && (u.height = /*height*/
        s[15]), _[0] & /*preview*/
        65536 && (u.preview = /*preview*/
        s[16]), _[0] & /*gap*/
        16384 && (u.gap = /*gap*/
        s[14]), _[0] & /*allow_preview*/
        131072 && (u.allow_preview = /*allow_preview*/
        s[17]), _[0] & /*show_share_button*/
        262144 && (u.show_share_button = /*show_share_button*/
        s[18]), _[0] & /*show_download_button*/
        1048576 && (u.show_download_button = /*show_download_button*/
        s[20]), _[0] & /*gradio*/
        8388608 && (u.i18n = /*gradio*/
        s[23].i18n), !n && _[0] & /*selected_index*/
        1 && (n = !0, u.selected_index = /*selected_index*/
        s[0], Vs(() => n = !1)), l.$set(u);
      },
      i(s) {
        i || (Ge(o), Ge(l.$$.fragment, s), i = !0);
      },
      o(s) {
        el(o), el(l.$$.fragment, s), i = !1;
      },
      d(s) {
        s && Rs(e), o && o.d(s), Hl(l, s);
      }
    }
  );
}
function Qs(t) {
  let e, l;
  return e = new An({
    props: {
      visible: (
        /*visible*/
        t[7]
      ),
      variant: "solid",
      padding: !1,
      elem_id: (
        /*elem_id*/
        t[5]
      ),
      elem_classes: (
        /*elem_classes*/
        t[6]
      ),
      container: (
        /*container*/
        t[10]
      ),
      scale: (
        /*scale*/
        t[11]
      ),
      min_width: (
        /*min_width*/
        t[12]
      ),
      allow_overflow: !1,
      $$slots: { default: [Ks] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      Xl(e.$$.fragment);
    },
    m(n, i) {
      Ul(e, n, i), l = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*visible*/
      128 && (o.visible = /*visible*/
      n[7]), i[0] & /*elem_id*/
      32 && (o.elem_id = /*elem_id*/
      n[5]), i[0] & /*elem_classes*/
      64 && (o.elem_classes = /*elem_classes*/
      n[6]), i[0] & /*container*/
      1024 && (o.container = /*container*/
      n[10]), i[0] & /*scale*/
      2048 && (o.scale = /*scale*/
      n[11]), i[0] & /*min_width*/
      4096 && (o.min_width = /*min_width*/
      n[12]), i[0] & /*loading_status, deletable, label, value, root, proxy_url, show_label, object_fit, _load_more_button_props, has_more, columns, height, preview, gap, allow_preview, show_share_button, show_download_button, gradio, selected_index*/
      33547039 | i[1] & /*$$scope*/
      16 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      l || (Ge(e.$$.fragment, n), l = !0);
    },
    o(n) {
      el(e.$$.fragment, n), l = !1;
    },
    d(n) {
      Hl(e, n);
    }
  };
}
function xs(t, e, l) {
  let { loading_status: n } = e, { show_label: i } = e, { has_more: o } = e, { label: a } = e, { elem_id: r = "" } = e, { elem_classes: f = [] } = e, { visible: s = !0 } = e, { value: _ = null } = e, { deletable: u } = e, { container: c = !0 } = e, { scale: d = null } = e, { min_width: w = void 0 } = e, { columns: p = [2] } = e, { gap: v = 8 } = e, { height: k = "auto" } = e, { preview: h } = e, { allow_preview: b = !1 } = e, { selected_index: m = null } = e, { show_share_button: L = !1 } = e, { object_fit: q = "cover" } = e, { show_download_button: F = !1 } = e, { root: Z } = e, { proxy_url: j } = e, { gradio: D } = e, { load_more_button_props: P = {} } = e, G = {};
  const ze = Js();
  function Y(y) {
    m = y, l(0, m);
  }
  const J = (y) => D.dispatch("click", y.detail), R = () => D.dispatch("change", _), B = (y) => D.dispatch("select", y.detail), Se = (y) => D.dispatch("share", y.detail), ve = (y) => D.dispatch("error", y.detail), je = (y) => D.dispatch("delete_image", y.detail), he = () => {
    D.dispatch("load_more", _);
  };
  return t.$$set = (y) => {
    "loading_status" in y && l(1, n = y.loading_status), "show_label" in y && l(2, i = y.show_label), "has_more" in y && l(3, o = y.has_more), "label" in y && l(4, a = y.label), "elem_id" in y && l(5, r = y.elem_id), "elem_classes" in y && l(6, f = y.elem_classes), "visible" in y && l(7, s = y.visible), "value" in y && l(8, _ = y.value), "deletable" in y && l(9, u = y.deletable), "container" in y && l(10, c = y.container), "scale" in y && l(11, d = y.scale), "min_width" in y && l(12, w = y.min_width), "columns" in y && l(13, p = y.columns), "gap" in y && l(14, v = y.gap), "height" in y && l(15, k = y.height), "preview" in y && l(16, h = y.preview), "allow_preview" in y && l(17, b = y.allow_preview), "selected_index" in y && l(0, m = y.selected_index), "show_share_button" in y && l(18, L = y.show_share_button), "object_fit" in y && l(19, q = y.object_fit), "show_download_button" in y && l(20, F = y.show_download_button), "root" in y && l(21, Z = y.root), "proxy_url" in y && l(22, j = y.proxy_url), "gradio" in y && l(23, D = y.gradio), "load_more_button_props" in y && l(25, P = y.load_more_button_props);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*_load_more_button_props, load_more_button_props*/
    50331648 && l(24, G = Object.assign(Object.assign({}, G), P)), t.$$.dirty[0] & /*selected_index*/
    1 && ze("prop_change", { selected_index: m });
  }, [
    m,
    n,
    i,
    o,
    a,
    r,
    f,
    s,
    _,
    u,
    c,
    d,
    w,
    p,
    v,
    k,
    h,
    b,
    L,
    q,
    F,
    Z,
    j,
    D,
    G,
    P,
    Y,
    J,
    R,
    B,
    Se,
    ve,
    je,
    he
  ];
}
class ef extends Ds {
  constructor(e) {
    super(), Hs(
      this,
      e,
      xs,
      Qs,
      Ws,
      {
        loading_status: 1,
        show_label: 2,
        has_more: 3,
        label: 4,
        elem_id: 5,
        elem_classes: 6,
        visible: 7,
        value: 8,
        deletable: 9,
        container: 10,
        scale: 11,
        min_width: 12,
        columns: 13,
        gap: 14,
        height: 15,
        preview: 16,
        allow_preview: 17,
        selected_index: 0,
        show_share_button: 18,
        object_fit: 19,
        show_download_button: 20,
        root: 21,
        proxy_url: 22,
        gradio: 23,
        load_more_button_props: 25
      },
      null,
      [-1, -1]
    );
  }
}
export {
  Bs as BaseGallery,
  ef as default
};
