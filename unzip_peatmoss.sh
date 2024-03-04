
# for dir in /scratch/gilbreth/jiang784/peatmoss_fortress/Zipped_PTM_Repos/*/; do 
#     for file in "$dir"*.tar.gz; do 
#         tar --strip-components=4 -xvzf  "$file" -C "/scratch/gilbreth/jiang784/peatmoss_fortress/huggingface_data/"; 
#     done; 
# done

for dir in /scratch/gilbreth/jiang784/peatmoss_fortress/Zipped_PTM_Repos/*/; do 
    for file in "$dir"*.tar.gz; do 
        # Assuming the unzipped content has a predictable name, construct its path
        # This example assumes that the unzipped content will have the same name as the .tar.gz file, minus the extension
        base_name=$(basename "$file" .tar.gz)
        unzipped_path="/scratch/gilbreth/jiang784/peatmoss_fortress/huggingface_data/$base_name"

        # Check if the unzipped content already exists
        if [ ! -d "$unzipped_path" ]; then
            echo "Unzipping $file..."
            tar --strip-components=4 -xvzf "$file" -C "/scratch/gilbreth/jiang784/peatmoss_fortress/huggingface_data/"
        else
            echo "Unzipped content for $file already exists, skipping..."
        fi
    done; 
done
