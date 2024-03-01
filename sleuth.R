library(sleuth)
library(dplyr)
setwd("PipelineProject_Madeline_Hakala")

# run sleuth 
stab = read.table('kallistoMetadata.txt', header = TRUE)
so = sleuth_prep(stab)
so = sleuth_fit(so, ~condition, 'full')
so = sleuth_fit(so, ~1, 'reduced')
so = sleuth_lrt(so, 'reduced', 'full')

# filter and extract results
sleuth_table = sleuth_results(so, 'reduced:full', 'lrt', show_all = FALSE)
sleuth_significant = dplyr::filter(sleuth_table, qval <= 0.05) |> dplyr::arrange(pval)
sleuth_significant_selected_collumns = dplyr::select(sleuth_significant, target_id, test_stat, pval, qval)
write.table(sleuth_significant_selected_collumns, file="resultsFDR05.txt", quote = FALSE, row.names = FALSE)
