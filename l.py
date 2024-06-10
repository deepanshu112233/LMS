# # data_list = [[31.5, 48.0, 1170.35, 0.0, 1433.33, 0.19, 0.55, -0.82, 0.06, 18.48, -7.8, 0.0, 244.0], [32.8, 48.0, 1165.46, 0.0, 1620.0, 0.19, 0.55, -0.82, 0.67, 19.7, -9.21, 0.0, 243.0], [31.8, 50.0, 1098.73, 0.0, 1588.33, 0.19, 0.55, -0.82, 2.13, 18.29, -8.11, 0.0, 237.0], [31.3, 49.0, 1134.76, 0.0, 1366.67, 0.19, 0.55, -0.83, 0.37, 20.55, -8.54, 0.0, 232.0], [31.1, 52.0, 1117.81, 0.0, 1664.17, 0.19, 0.55, -0.83, 0.79, 17.38, -7.87, 0.0,
# data_list = [[31.5, 48.0, 1170.35, 0.0, 1433.33, 0.19, 0.55, -0.82, 0.06, 18.48, -7.8, 0.0, 244.0],
#              [32.8, 48.0, 1165.46, 0.0, 1620.0, 0.19,
#                  0.55, -0.82, 0.67, 19.7, -9.21, 0.0, 243.0],
#              [31.8, 50.0, 1098.73, 0.0, 1588.33, 0.19,
#                  0.55, -0.82, 2.13, 18.29, -8.11, 0.0, 237.0],
#              [31.3, 49.0, 1134.76, 0.0, 1366.67, 0.19,
#               0.55, -0.83, 0.37, 20.55, -8.54, 0.0, 232.0],
#              [31.1, 52.0, 1117.81, 0.0, 1664.17, 0.19,
#               0.55, -0.83, 0.79, 17.38, -7.87, 0.0, 222.0],
#              [30.7, 53.0, 1104.22, 0.0, 1803.33, 0.19,
#               0.55, -0.82, 1.52, 19.76, -8.17, 0.0, 217.0],
#              [30.8, 52.0, 1126.59, 0.0, 1835.83, 0.19,
#               0.55, -0.81, 1.77, 18.84, -8.66, 0.0, 210.0],
#              [30.2, 53.0, 1091.28, 0.0, 690.83, 0.18,
#               0.54, -0.82, 2.56, 18.96, -9.76, 0.0, 229.0],
#              [29.2, 55.0, 1127.7, 0.0, 1368.33, 0.19,
#               0.55, -0.82, 2.62, 19.45, -9.51, 0.0, 224.0],
#              [28.8, 52.0, 1104.53, 0.0, 89.17, 0.18, 0.54, -0.82, 2.93, 18.05, -8.48, 0.0, 194.0]]

# data_array = np.array(data_list)
# data_array = data_array.reshape((-1, 10, 13)).astype(np.float32)
# data_torch = torch.tensor(data_array)
# print("Manual input 2: ", data_torch.size())
# # print(data_torch)

# # Make predictions
# with torch.no_grad():
#     (weather_output_10, weather_output_30, weather_output_60,
#      landslide_output_10, landslide_output_30, landslide_output_60) = model(data_torch)

#     # Convert outputs to numpy arrays and move to CPU
#     weather_output_10 = weather_output_10.cpu().numpy()
#     weather_output_30 = weather_output_30.cpu().numpy()
#     weather_output_60 = weather_output_60.cpu().numpy()
#     landslide_output_10 = torch.argmax(
#         landslide_output_10, dim=1).cpu().numpy()
#     landslide_output_30 = torch.argmax(
#         landslide_output_30, dim=1).cpu().numpy()
#     landslide_output_60 = torch.argmax(
#         landslide_output_60, dim=1).cpu().numpy()

# # Display the predictions
# # print("Predicted weather parameters for 10 minutes ahead:", weather_output_10)
# formatted_data_format_10 = [
#     ["{:.2f}".format(num) for num in row] for row in weather_output_10]
# print("Formatted Data (format method):", formatted_data_format_10)
# prediction = formatted_data_format_10

# # print("Predicted weather parameters for 30 minutes ahead:", weather_output_30)
# formatted_data_format_30 = [
#     ["{:.2f}".format(num) for num in row] for row in weather_output_30]
# print("Formatted Data (format method):", formatted_data_format_30)

# # print("Predicted weather parameters for 60 minutes ahead:", weather_output_60)
# formatted_data_format_60 = [
#     ["{:.2f}".format(num) for num in row] for row in weather_output_60]
# print("Formatted Data (format method):", formatted_data_format_60)


# print("Predicted landslide class for 10 minutes ahead:", landslide_output_10)
# print("Predicted landslide class for 30 minutes ahead:", landslide_output_30)
# print("Predicted landslide class for 60 minutes ahead:", landslide_output_60)




