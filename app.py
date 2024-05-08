from flask import Flask, request, jsonify
import rembg
import os

# Define output folder path
OUTPUT_FOLDER = 'processed_images'  # Adjust this path as needed

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if request.method == 'POST':
        try:
            # Handle potential file upload errors
            image_file = request.files['image']
            if image_file.filename == '':
                return jsonify({'success': False, 'message': 'No selected image file'}), 400

            # Read image data in binary mode
            image_bytes = image_file.read()

            # Remove background using Rembg
            output = rembg.remove(image_bytes)

            # Generate a unique output filename
            import uuid
            output_filename = f'{uuid.uuid4()}.png'

            # Create output folder if it doesn't exist
            os.makedirs(OUTPUT_FOLDER, exist_ok=True) 

            # Save the processed image to output folder
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            with open(output_path, 'wb') as o:
                o.write(output)

            # Return success response with image path in output folder
            return jsonify({'success': True, 'image_path': os.path.join(OUTPUT_FOLDER, output_filename)})

        except Exception as e:
            print(f"Error removing background: {e}")
            return jsonify({'success': False, 'message': 'Background removal failed'}), 500

    return jsonify({'success': False, 'message': 'Invalid request method'}), 405

if __name__ == '__main__':
    app.run(debug=True)
