import click

def highlight_errors(pred: str, label: str) -> str:
  """Returns `pred` but highlights errors in red."""
  highlighted_prediction = ""
  for lbl_char, pred_char in zip(label, pred):
      if lbl_char == pred_char:
          highlighted_prediction += pred_char
      else:
          highlighted_prediction += click.style(pred_char, fg='red')
  # Handle the case where pred is longer than label
  if len(pred) > len(label):
      highlighted_prediction += click.style(pred[len(label):], fg='red')
  return highlighted_prediction

