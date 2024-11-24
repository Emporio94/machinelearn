import dyn_plot
import numpy as np 

_CONVERGENCE_SILENT = False

# context manager that sets/unsets the _CONVERGENCE_SILENT flag
class no_graph:
    def __enter__(self):
        global _CONVERGENCE_SILENT
        self.prev = _CONVERGENCE_SILENT
        _CONVERGENCE_SILENT = True
    def __exit__(self, *args):
        global _CONVERGENCE_SILENT
        _CONVERGENCE_SILENT = self.prev

def unicode_plot(values, width=60, height_range=(0x2581, 0x2588)):
    # Resample the input values to match the desired width
    if len(values)>width:
        resampled_values = np.interp(np.linspace(0, len(values) - 1, width), range(len(values)), values)
    else:
        resampled_values = values
    
    # Normalize values to the Unicode character range
    min_val, max_val = min(resampled_values), max(resampled_values)
    span = height_range[1] - height_range[0]

    # Handle constant values by using the mid-character
    if min_val == max_val:
        return chr(height_range[0] + span // 2) * width

    # Map each value to a character
    unicode_plot = ''.join(
        chr(int((val - min_val) / (max_val - min_val) * span) + height_range[0])
        for val in resampled_values
    )

    return unicode_plot[:width].ljust(width)

class Convergence:
    def __init__(self, graph=True, interval=1, silent=False):
        self.loss = []
        self.graph = graph 
        self.interval = interval    
        self.silent = silent
        if graph and not self.silent and not _CONVERGENCE_SILENT:
            self.plot = dyn_plot.Plot(figsize=(10,2))
            

    def update(self, l):
        self.loss.append(l)
        if self.silent or _CONVERGENCE_SILENT:
            print(f"Iter: {len(self.loss):8d}  Loss: {l:12.4f}      ", end="\r")
            return 
        if len(self.loss) % self.interval == 0:
            avg_loss = np.mean(self.loss[-self.interval:])
            reshaped_loss = np.reshape(self.loss, (-1, self.interval)).mean(axis=1)
            if self.graph:
                
                    with self.plot:
                        l = len(reshaped_loss)
                        self.plot.plot(np.arange(l)*self.interval, reshaped_loss, lw=2, c='C0')
                        self.plot.plot(np.linspace(0, len(self.loss), len(self.loss)), self.loss, alpha=0.2, lw=1, c='C0')
                        
                        self.plot.set_title(f"Iteration {len(self.loss):8d}      Loss: {avg_loss:12.4f}")
                        self.plot.set_xlabel("Iteration #")
                        self.plot.set_ylabel("Loss")
                        self.plot.set_ylim(bottom=0)
            else:
                
                print(f"Iter: {len(self.loss):8d}  Loss: {avg_loss:12.4f}  Graph: {unicode_plot(reshaped_loss)}", end="\r")

    def reset(self):
        self.loss = []
    def close(self):
        if self.graph and not self.silent and not _CONVERGENCE_SILENT:
            self.plot.close()