import sublime
import sublime_plugin
import re

selection_added = False

class AppendSeletion(sublime_plugin.TextCommand):
  def __init__(self, view):
    super().__init__(view)
    self.last_word = None

  def run(self, edit, word = False, backward = False, skip = False,
    repeat_last_with_skip = False):

    if repeat_last_with_skip:
      word = self.last_word
      backward = self.last_backward
      skip = True

    self.last_word = word
    self.last_backward = backward

    sels = self.view.sel()
    if len(sels) == 0:
      return

    result = self._get_next_selection(sels, word, backward)

    if result == None:
      return

    sel, matches, shift = result
    self._append_selection(skip, sel, matches, shift)

    global selection_added
    selection_added = True

  def _append_selection(self, skip, sel, matches, shift):
    try:
      match = matches.__next__()
    except StopIteration:
      return

    start, end = match.start(1) + shift, match.end(1) + shift
    if sel.a > sel.b:
      start, end = end, start

    selection = sublime.Region(start, end)
    if skip:
      self.remove_last_selection()

    self.view.sel().add(selection)

    regions = []
    for match in matches:
      start, end = match.start(1) + shift, match.end(1) + shift
      regions.append(sublime.Region(start, end))

    self.view.erase_regions('append_selection')
    self.view.add_regions('append_selection', regions, 'string', '',
      sublime.DRAW_EMPTY)

  def remove_last_selection(self):
    sels = self.view.sel()

    old = []
    for index, sel in enumerate(sels):
      if index == len(sels) - 1:
        continue
      old.append(sel)

    self.view.sel().clear()
    for sel in old:
      self.view.sel().add(sel)

  def _get_next_selection(self, sels, word, backward):
    if backward:
      sel = sels[0]
    else:
      sel = sels[-1]

    if sel.empty():
      sel = self.view.word(sel.b)
      if sel.empty():
        return None
      if backward:
        cursor = sel.end()
      else:
        cursor = sel.begin()
    else:
      if backward:
        cursor = sel.begin()
      else:
        cursor = sel.end()

    selected = self.view.substr(sel)
    if backward:
      region = sublime.Region(0, cursor)
    else:
      region = sublime.Region(cursor, self.view.size())

    text = self.view.substr(region)

    if word:
      matches = re.finditer(r'\W(' + re.escape(selected) + r')\W', text)
    else:
      matches = re.finditer(r'(' + re.escape(selected) + r')', text)

    if backward:
      matches = reversed(list(matches))

    return sel, matches, region.a

class AppendSeletionListener(sublime_plugin.EventListener):
  def on_selection_modified_async(self, view):
    global selection_added
    if selection_added:
      selection_added = False
      return

    view.erase_regions('append_selection')