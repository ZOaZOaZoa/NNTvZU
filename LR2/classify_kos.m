function target_m = classify_kos(target)
    for i=1:1000
        if (target(i)< 0.95)
            target_m(i)=0
        elseif (target(i)<0.97)
            target_m(i)=1
        elseif (target(i)<0.99)
            target_m(i)=2
        else
            target_m(i)=3
        end
    end
 target_m = target_m'
end