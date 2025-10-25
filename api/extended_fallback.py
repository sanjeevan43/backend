from flask import jsonify

def get_reverse_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def reverseString(self, s):
        left, right = 0, len(s) - 1
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1
        return s
```

Time Complexity: O(n)
Space Complexity: O(1)

Explanation: Use two pointers to swap characters from both ends moving towards center.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_max_subarray_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def maxSubArray(self, nums):
        max_sum = current_sum = nums[0]
        
        for i in range(1, len(nums)):
            current_sum = max(nums[i], current_sum + nums[i])
            max_sum = max(max_sum, current_sum)
        
        return max_sum
```

Time Complexity: O(n)
Space Complexity: O(1)

Explanation: Kadane's algorithm - keep track of current sum and maximum sum seen so far.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_binary_search_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def search(self, nums, target):
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1
```

Time Complexity: O(log n)
Space Complexity: O(1)

Explanation: Classic binary search - divide search space in half each iteration.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_merge_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def merge(self, nums1, m, nums2, n):
        i, j, k = m - 1, n - 1, m + n - 1
        
        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1
        
        while j >= 0:
            nums1[k] = nums2[j]
            j -= 1
            k -= 1
```

Time Complexity: O(m + n)
Space Complexity: O(1)

Explanation: Merge from the end to avoid overwriting elements in nums1.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_climbing_stairs_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def climbStairs(self, n):
        if n <= 2:
            return n
        
        prev2, prev1 = 1, 2
        for i in range(3, n + 1):
            current = prev1 + prev2
            prev2, prev1 = prev1, current
        
        return prev1
```

Time Complexity: O(n)
Space Complexity: O(1)

Explanation: Dynamic programming - each step is sum of previous two steps (Fibonacci pattern).'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_stock_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def maxProfit(self, prices):
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price
        
        return max_profit
```

Time Complexity: O(n)
Space Complexity: O(1)

Explanation: Track minimum price seen so far and maximum profit possible.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_duplicate_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def containsDuplicate(self, nums):
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
```

Time Complexity: O(n)
Space Complexity: O(n)

Explanation: Use set to track seen numbers, return True if duplicate found.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_product_except_self_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)
        result = [1] * n
        
        # Left products
        for i in range(1, n):
            result[i] = result[i-1] * nums[i-1]
        
        # Right products
        right = 1
        for i in range(n-1, -1, -1):
            result[i] *= right
            right *= nums[i]
        
        return result
```

Time Complexity: O(n)
Space Complexity: O(1)

Explanation: Two passes - first for left products, second for right products.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_min_rotated_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def findMin(self, nums):
        left, right = 0, len(nums) - 1
        
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid
        
        return nums[left]
```

Time Complexity: O(log n)
Space Complexity: O(1)

Explanation: Binary search to find the pivot point where rotation occurred.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_container_water_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def maxArea(self, height):
        left, right = 0, len(height) - 1
        max_area = 0
        
        while left < right:
            area = min(height[left], height[right]) * (right - left)
            max_area = max(max_area, area)
            
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        
        return max_area
```

Time Complexity: O(n)
Space Complexity: O(1)

Explanation: Two pointers approach - move pointer with smaller height inward.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_three_sum_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def threeSum(self, nums):
        nums.sort()
        result = []
        
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            
            left, right = i + 1, len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
        
        return result
```

Time Complexity: O(n²)
Space Complexity: O(1)

Explanation: Sort array, then use two pointers for each element to find triplets that sum to zero.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_longest_substring_solution(language):
    solutions = {
        'python': '''```python
class Solution:
    def lengthOfLongestSubstring(self, s):
        char_map = {}
        left = max_length = 0
        
        for right in range(len(s)):
            if s[right] in char_map and char_map[s[right]] >= left:
                left = char_map[s[right]] + 1
            
            char_map[s[right]] = right
            max_length = max(max_length, right - left + 1)
        
        return max_length
```

Time Complexity: O(n)
Space Complexity: O(min(m,n))

Explanation: Sliding window with hash map to track character positions and avoid duplicates.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})