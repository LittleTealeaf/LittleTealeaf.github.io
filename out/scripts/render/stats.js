function render_stats(data) {
  const {references, stats} = data;


  return render_dom({
    amp: "_stats",
    classList: ["&"],
  });
}
