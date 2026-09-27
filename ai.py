"""from sklearn.linear_model import LinearRegression

# Training data
X = list(map(float, input("Enter X values: ").split()))
y = [20, 30, 40, 50, 60]

# Convert X to 2D
X = [[value] for value in X]

# Create model
model = LinearRegression()

# Train
model.fit(X, y)

# Prediction
prediction = model.predict([[6]])

print("Prediction:", prediction)
print("X:", X)"""
from sklearn.linear_model import LinearRegression


X = []
y = []

n = int(input("How many data points? "))

for i in range(n):
    x = float(input(f"Enter x value {i+1}: "))
    y_value = float(input(f"For x = {x}, enter y value: "))

    X.append([x])
    y.append(y_value)
#amitdiksdfvsd
# Create model
model = LinearRegression()

# Train model
model.fit(X, y)

# Prediction
x_new = float(input("Enter x to predict y: "))

prediction = model.predict([[x_new]])

print("Predicted y =", round(prediction[0], 2))
print("Slope:", round(model.coef_[0],2))
print("Intercept:", round(model.intercept_,2))
2

"""
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

X = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
y = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Test data:", X_test)
print("Actual:", y_test)
print("Predicted:", predictions)"""