import{$ as e,B as t,D as n,G as r,S as i,b as a,bt as o,et as s,v as c,vt as l,y as u}from"./modules/shiki-B7M4eKE7.js";import{n as d,t as f}from"./context-CJeW49dK.js";import{t as p}from"./default-YSQUVGnO.js";import{t as m}from"./Callout-BtHAaUW0.js";var h={__name:`cp26-cumulative.md__slidev_14`,setup(h){let{$slidev:g,$nav:_,$clicksContext:v,$clicks:y,$page:b,$renderContext:x,$frontmatter:S}=d();return v.setup(),(d,h)=>{let g=m,_=r(`click`);return t(),u(p,o(n(l(f)(l(S),13))),{default:e(()=>[h[3]||=c(`h1`,null,`Takeaways`,-1),a(`
  This slide and the next are one beat: the three takeaways land full-width
  here, then morph — same three cards, squeezed into a column — to make room
  for the QR. The morph is the View Transitions API: each card carries a
  \`view-transition-name\` that also exists on the next slide, so the browser
  tweens the two boxes instead of cross-fading the slides.

  Two things this depends on, both easy to break:
    • the name must match its twin on the next slide, and be unique per slide;
    • \`transition: view-transition\` belongs on THIS slide, not the next one —
      Slidev reads the transition off the lower-numbered slide of a pair in
      both directions (see useViewTransition.ts), so putting it on slide 15
      silently does nothing.
  Chrome-only; other browsers just fall back to the deck's slide-up.
`),s((t(),u(g,{style:{"view-transition-name":`takeaway-1`}},{default:e(()=>[...h[0]||=[c(`p`,null,[c(`code`,null,`Cumulative`),i(` constraints can be seen as `),c(`strong`,null,`linear inequalities over occupancy vectors`),i(` and handled with polyhedral methods`)],-1)]]),_:1})),[[_]]),s((t(),u(g,{style:{"view-transition-name":`takeaway-2`}},{default:e(()=>[...h[1]||=[c(`p`,null,[c(`strong`,null,`Lifting`),i(` generalizes classical bounds (LB4/LB5) into a CP-native, root-node inference`)],-1)]]),_:1})),[[_]]),s((t(),u(g,{style:{"view-transition-name":`takeaway-3`}},{default:e(()=>[...h[2]||=[c(`p`,null,[c(`strong`,null,`A helpful preprocessing technique`),i(` with improved robustness over UnL`)],-1)]]),_:1})),[[_]])]),_:1},16)}}};export{h as default};